from flask import Blueprint

api_upload_csv = Blueprint("api_upload_csv",__name__)

from . import upload_csv

