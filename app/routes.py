from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, request, jsonify, flash
from pandas import DataFrame

from app import app, db
from .stock_api import get_alerts, insert_stock, delete_stocks, get_alerts_old
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
        if form.validate_on_submit():
            insert_stock(form.market.data,
                        form.stock_code.data,
                        form.entry_price.data)
            return redirect(url_for('manage_list'))
        else:
            flash("Invalid CODE")
    asx_list = Stock.query.filter_by(market='asx').all()
    nasdaq_list = Stock.query.filter_by(market='nasdaq').all()
    return render_template("list.html", data=[asx_list, nasdaq_list], form=form)

@app.route('/current_alerts')
def current_alerts():
    data = get_alerts()
    print(data)
    return render_template("alerts.html", alerts = data, alerts24 = data)

@app.route('/test')
def test():
    print(get_alerts())
    return render_template('test.html')

@app.route('/delete_stocks', methods=['POST'])
def del_stocks():
    ids = request.form['ids'].split(',')
    delete_stocks([int(x) for x in ids])
    return jsonify({'resp': 'done'})