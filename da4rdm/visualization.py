##ConformanceChecking ..added by Mrunmai
import os
from os.path import isfile, join
from flask import (
	Blueprint, render_template,request
)

import da4rdm.api.api as api
from da4rdm.api import user_session

bp = Blueprint('blueprints/main', __name__)

visualization_bp = Blueprint('blueprints/visualization',__name__, template_folder='templates', static_folder='static')

@visualization_bp.route('/')
def visualization():
    unique_projects = api.get_unique_projects()
    print('projects', unique_projects)
    return render_template('visualization/visualization.html',operation_list=unique_projects)

