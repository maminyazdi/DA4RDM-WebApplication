import os
import re
import csv
import sqlalchemy
import importlib
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4ds import db
import da4ds.api.api as api
bp = Blueprint('blueprints/main', __name__)

@bp.route('/')
def index():
    data_sources = api.get_all_data_sources()
    pipeline_names = api.get_all_pipeline_names()
    return render_template('preprocessing/preprocessing.html', data_sources=data_sources, pipelines=pipeline_names) # until more functionality is included, the base url redirects to the preprocessing page, as that is the entry point for all currently supported functionality