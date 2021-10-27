from requests import get

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

r = get('https://api.iextrading.com/1.0/ref-data/symbols')
app.stock_codes = set([x['symbol'] for x in r.json()])