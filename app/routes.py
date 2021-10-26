from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, request, jsonify
from pandas import DataFrame

from app import app, db
from .stock_api import get_alerts, get_list
from .forms import InvestmentForm, AddStockForm
from .models import Stock

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/historical_performance', methods=['GET', 'POST'])
def historical_performance():
    form = InvestmentForm()
    display = 'none'
    if form.validate_on_submit():
        display = ''
    return render_template('historic_performance.html', form=form, display=display)

@app.route('/manage_list', methods=['GET', 'POST'])
def manage_list():
    form = AddStockForm()
    if request.method == 'POST':
        print(form.market.data)
        print(form.stock_code.data)
        print(form.entry_price.data)
        print(form.validate())
        if form.validate_on_submit():
            print('asdawr')
    asx_list = Stock.query.filter_by(market='asx').all()
    nasdaq_list = Stock.query.filter_by(market='nasdaq').all()
    return render_template("list.html", data=[asx_list, nasdaq_list], form=form)

@app.route('/current_alerts')
def current_alerts():
    codes = ['MSFT', 'GOOG', 'HOG', 'KO', 'T', 'WMT', 'AAPL', 'HPQ', 'V', 'F']
    data = get_alerts(codes)
    data24H = data[data['Date'] > datetime.now() - timedelta(1)]
    return render_template("alerts.html", alerts = data, alerts24 = data24H)

@app.route('/test')
def test():
    return render_template('test.html')

# @app.route('/add_stock', methods=["POST"])
# def cadd_stock():
    # new_stock = Stock(market=request.form['market'],
                    # stock_code=request.form['code'],
                    # entry_price=request.form['price'])
    # db.session.add(new_stock)
    # db.session.commit()
    # return redirect(url_for('manage_list'))
    # return render_template('list.html')
    # return jsonify({'text': 'added'})

@app.route('/delete_stocks', methods=['POST'])
def del_stocks():
    print('asdaaaaaaaaaaaaaaaa')
    print(request.form.getlist('row-check'))
    return render_template('list.html')