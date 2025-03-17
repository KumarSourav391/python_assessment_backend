from flask import Blueprint

api_home = Blueprint("api_home",__name__)

from . import health_check