from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, RadioField, SubmitField, TextField, ValidationError
from wtforms.validators import DataRequired

from app import app

class InvestmentForm(FlaskForm):
    amount = IntegerField('Hypothetical Investment Amount: ', validators=[DataRequired()])
    trade_type = RadioField('Trades directions to include', choices=[('sell', 'Sell'), ('buy', 'Buy'), ('both', 'Both')])
    submit = SubmitField('View result')

class AddStockForm(FlaskForm):
    market = RadioField('Market', choices=[('nasdaq', 'Nasdaq'), ('asx', 'ASX')])
    stock_code = TextField('Stock Code' , validators=[DataRequired()])
    entry_price = FloatField('Entry Price', validators=[DataRequired()])
    submit = SubmitField('Add Stock')

    def validate_stock_code(form, field):
        if field not in app.stock_codes:
            raise ValidationError("Invalid Stock Code!")