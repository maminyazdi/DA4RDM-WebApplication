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

process_mining_bp = Blueprint('blueprints/process_mining', __name__, template_folder='templates', static_folder='static')

@process_mining_bp.route('/')
def process_mining():
    return render_template('process_mining/process_mining.html')

@process_mining_bp.route('/process_discovery')
def process_discovery():
    return render_template('process_mining/process_discovery.html')
