from datetime import date

from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    __table_args__ = (
        db.UniqueConstraint('market', 'stock_code'),
    )
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(16), nullable=False)
    stock_code = db.Column(db.String(8), index=True)
    company_name = db.Column(db.String(50))
    entry_price = db.Column(db.Float, nullable=False)
    alerts = db.relationship('Alert', backref='stocks', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'{self.id}:{self.market}:{self.stock_code}:{self.entry_price}'

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    trade_type = db.Column(db.String(4), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False)
    alert_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'{self.date}:{self.trade_type}:{self.stock_id}:{self.alert_price}'