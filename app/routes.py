from flask import render_template
from requests.api import get
from app import app
from .stock_api import get_alerts

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/historical_performance')
def historical_performance():
    return "LIE"

@app.route('/manage_list')
def manage_list():
    return "DO"

@app.route('/current_alerts')
def current_alerts():
    codes = ['MSFT']
    data = get_alerts(codes)
    return render_template("alerts.html", shape = data.shape)