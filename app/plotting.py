import pandas_ta as ta
from bokeh.plotting import figure
from bokeh.layouts import gridplot
import yfinance as yf

def bokeh_plot(df, stock_code, plot_width, plot_height):
#     print(df.head())
    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 18*60*60*1000
    p1 = figure(x_axis_type="datetime", width=plot_width, height=plot_height, title ='{} Daily Chart'.format(stock_code))
    p1.segment(df.index, df.High, df.index, df.Low, color="black")
    p1.vbar(df.index[inc], w, df.Open[inc], df.Close[inc], fill_color="lawngreen", line_color="lawngreen")
    p1.vbar(df.index[dec], w, df.Open[dec], df.Close[dec], fill_color="tomato", line_color="tomato")
    p1.line(df.index, df['EMA10'], color="black", legend_label="EMA 10", line_width=2, line_alpha=0.5, line_dash='dashed')
    p1.line(df.index, df['EMA50'], color="red", legend_label="EMA 50", line_width=2, line_alpha=0.5, line_dash='dashed')
 
    p1.triangle(df.index[df.buy_K], df.Close[df.buy_K], size = 10, color = 'green', legend_label='Long') 
    p1.triangle(df.index[df.sell_K], df.Close[df.sell_K], size = 10, color = 'red', legend_label='Short')
    
    #return p1

    p2 = figure(x_axis_type="datetime", x_range=p1.x_range, width=plot_width, height=plot_height//2, title ='{} K'.format(stock_code))
    p2.line(df.index, df['STOCHk_14_3_3'], color="tomato", legend_label="K 14-3-3", line_width=2)
    p2.line(df.index, df['STOCHk_50_3_3'], color="lawngreen", legend_label="K 50-3-3", line_width=2)
    p2.triangle(df.index[df.buy_K], [0]*sum(df.buy_K), size = 10, color = 'green', legend_label='Long') 
    p2.triangle(df.index[df.sell_K], [0]*sum(df.sell_K), size = 10, color = 'red', legend_label='Short') 
    
    #output_file(filename=f"stock_charts{stock_code}.html", title="Static HTML file")

    return gridplot([p1, p2], ncols=1,) # plot_width=plot_width, plot_height=plot_height)


def save_plot_signals(stock_code, period="2000d", plot_width=800, plot_height=500):
    """Define signals, plot candlestick graph and save CSV file"""
    msft = yf.Ticker(stock_code)
    # get historical market data
    hist = msft.history(period=period)

    # Add EMA 10 
    hist['EMA10'] = hist.ta.ema(close='Close', length=10)
    hist['EMA50'] = hist.ta.ema(close='Close', length=50)

    # Generate K stichastic oscilators and write it in hist DataFrame
    hist.ta.stoch(high='high', low='low', k=14, d=3, append=True)
    hist.ta.stoch(high='high', low='low', k=50, d=3, append=True)

    hist['buy_K'] = hist.apply(lambda x: x['STOCHk_14_3_3']>70 and x['STOCHk_50_3_3'] < 30, axis=1)
    hist['sell_K'] = hist.apply(lambda x: x['STOCHk_14_3_3']<30 and x['STOCHk_50_3_3'] > 70, axis=1)

    # plot
    return bokeh_plot(hist, stock_code, plot_width, plot_height)
