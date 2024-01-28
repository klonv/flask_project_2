import os, click
# from app import app
from flask import Blueprint

bp = Blueprint('cli', __name__, cli_group=None)

# @app.cli.group()
@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass

# подкоманда инициализации
@translate.command()
@click.argument('lang')
def init(lang):
    # initialize a new language
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')

# обновить и скомпилировать подкоманды
@translate.command()
def update():
    # update all languages
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate.command()
def compile():
    # compile all languages
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')
    

