from flask import Blueprint

# схема ошибок
bp = Blueprint('errors', __name__)

from app.errors import handlers