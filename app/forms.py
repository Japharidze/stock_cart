from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, RadioField, SubmitField, TextField
from wtforms.validators import DataRequired

class InvestmentForm(FlaskForm):
    amount = IntegerField('Hypothetical Investment Amount: ', validators=[DataRequired()])
    trade_type = RadioField('Trades directions to include', choices=[('sell', 'Sell'), ('buy', 'Buy'), ('both', 'Both')])
    submit = SubmitField('View result')

class AddStockForm(FlaskForm):
    market = RadioField('Market', choices=[('nasdaq', 'Nasdaq'), ('asx', 'ASX')])
    stock_code = TextField('Stock Code' , validators=[DataRequired()])
    entry_price = FloatField('Entry Price', validators=[DataRequired()])
    submit = SubmitField('Add Stock')
