from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired

class InvestmentForm(FlaskForm):
    amount = IntegerField('Hypothetical Investment Amount: ', validators=[DataRequired()])
    trade_type = RadioField('Trades directions to include', choices=[('sell', 'Sell'), ('buy', 'Buy'), ('both', 'Both')])
    submit = SubmitField('View result')