
from flask import Flask, current_app, request
# from app.errors import handlers
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

import os
import pypugjs
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'ru'



db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
moment = Moment()
babel = Babel()

def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension') 

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
        # регистрировать ошибки по электронной почте.
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            # if app.config['MAIL_USE_SSL']:
            #     secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Site_flask Failure', credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        # Запись в файл
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/site_flask.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s' '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.addHandler('Site_flask startup')

    return app

from app import models