from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, RadioField, SubmitField, TextField, ValidationError
from wtforms.validators import DataRequired
from yfinance import download

from app import app

class InvestmentForm(FlaskForm):
    amount = IntegerField('Hypothetical Investment Amount: ', validators=[DataRequired()])
    trade_type = RadioField('Trades directions to include', choices=[('Sell', 'Sell'), ('Buy', 'Buy'), ('Both', 'Both')])
    submit = SubmitField('View result')

class AddStockForm(FlaskForm):
    market = RadioField('Market', choices=[('nasdaq', 'Nasdaq'), ('asx', 'ASX')], validators=[DataRequired(message="Choose the market!")])
    stock_code = TextField('Stock Code' , validators=[DataRequired(message="Fill the Code!")])
    submit = SubmitField('Add Stock')

    def validate_stock_code(self, code):
        info = download(code, period='1m', interval='1m')
        if info.shape[0] == 0:
            raise ValidationError("Invalid Stock Code!")