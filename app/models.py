from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    __table_args__ = (
        db.UniqueConstraint('market', 'stock_code'),
    )
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(16), nullable=False)
    stock_code = db.Column(db.String(8), index=True)
    entry_price = db.Column(db.Float, nullable=False)
    alerts = db.relationship('Alerts', backref='stocks', lazy=True)

    def __repr__(self):
        return f'{self.market} - {self.stock_code} - {self.entry_price}'

class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trade_type = db.Column(db.String(4), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False)
    alert_price = db.Column(db.Float, nullable=False)