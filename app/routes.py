import json
from flask import render_template, redirect, url_for, request, jsonify
from bokeh.embed import json_item

from app import app
from .stock_api import get_alerts, insert_stock, delete_stocks, historical_model
from .forms import InvestmentForm, AddStockForm
from .models import Stock
from .plotting import save_plot_signals

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/historical_performance', methods=['GET', 'POST'])
def historical_performance():
    form = InvestmentForm()
    periodic_data = None
    if form.validate_on_submit():
        trade_type = form.trade_type.data
        periodic_data = historical_model(trade_type=trade_type)
        # return redirect(url_for('historical_performance'))
    form.amount.data = None
    return render_template('historic_performance.html',
                            form=form,
                            data=periodic_data)

@app.route('/manage_list', methods=['GET', 'POST'])
def manage_list():
    form = AddStockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            insert_stock(form.market.data,
                        form.stock_code.data.upper())
            return redirect(url_for('manage_list'))
    asx_list = Stock.query.filter_by(market='asx').order_by(Stock.id).all()
    nasdaq_list = Stock.query.filter_by(market='nasdaq').order_by(Stock.id).all()
    return render_template("list.html", data=[asx_list, nasdaq_list], form=form)

@app.route('/current_alerts')
def current_alerts():
    day, week = get_alerts()
    return render_template("alerts.html", alerts=week, alerts24=day)

@app.route('/test')
def test():
    print(get_alerts())
    return render_template('test.html')

@app.route('/delete_stocks', methods=['POST'])
def del_stocks():
    ids = request.form['ids'].split(',')
    delete_stocks([int(x) for x in ids])
    return jsonify({'resp': 'done'})

@app.route('/plot/<code>')
def plot(code):
    p = save_plot_signals(code, period="200d")
    return json.dumps(json_item(p, "myplot"))
