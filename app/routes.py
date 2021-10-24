from datetime import datetime, timedelta

from flask import render_template, request, jsonify
from pandas import DataFrame

from app import app, db
from .stock_api import get_alerts, get_list
from .forms import InvestmentForm
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

@app.route('/manage_list')
def manage_list():
    asx_list = Stock.query.filter_by(market='asx').all()
    nasdaq_list = Stock.query.filter_by(market='nasdaq').all()
    return render_template("list.html", data=[asx_list, nasdaq_list])

@app.route('/current_alerts')
def current_alerts():
    codes = ['MSFT', 'GOOG', 'HOG', 'KO', 'T', 'WMT', 'AAPL', 'HPQ', 'V', 'F']
    data = get_alerts(codes)
    data24H = data[data['Date'] > datetime.now() - timedelta(1)]
    return render_template("alerts.html", alerts = data, alerts24 = data24H)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/add_stock', methods=["POST"])
def add_stock():
    new_stock = Stock(market=request.form['market'],
                    stock_code=request.form['code'],
                    entry_price=request.form['price'])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'text': 'added'})