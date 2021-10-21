from datetime import datetime, timedelta

from flask import render_template, request
from pandas import DataFrame

from app import app
from .stock_api import get_alerts, get_list
from .forms import InvestmentForm

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
    data = DataFrame(get_list())
    data2 = DataFrame(get_list())
    return render_template("list.html", data=[data, data2])

@app.route('/current_alerts')
def current_alerts():
    codes = ['MSFT', 'GOOG', 'HOG', 'KO', 'T', 'WMT', 'AAPL', 'HPQ', 'V', 'F']
    data = get_alerts(codes)
    data24H = data[data['Date'] > datetime.now() - timedelta(1)]
    return render_template("alerts.html", alerts = data, alerts24 = data24H)