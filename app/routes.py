from flask import render_template
from app import app

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
    return "DONT"