from flask import render_template, redirect, url_for, request, jsonify

from app import app
from .stock_api import get_alerts, insert_stock, delete_stocks
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
                        form.stock_code.data)
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