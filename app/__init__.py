
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import pypugjs

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models