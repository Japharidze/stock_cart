from app import db

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(16), nullable=False)
    stock_code = db.Column(db.String(8), index=True, unique=True)
    entry_price = db.Column(db.Float, nullable=False)
    alerts = db.relationship('Alerts', backref='stock', lazy=True)

    def __repr__(self):
        return f'{self.market} - {self.stock_code}'

class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trade_type = db.Column(db.String(4), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    alert_price = db.Column(db.Float, nullable=False)