##Visualization ..added by Mrunmai
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
    unique_projects, start_date, end_date = api.get_unique_projects()
    """combined_list = []
    for i in range(len(start_date)):
        combined_list.append('Project' + unique_projects[i+1] + 'StartDate:' + start_date[i] + 'EndDate:' + end_date[i])
    print('combined',combined_list)"""
    return render_template('visualization/visualization.html',project_list=unique_projects)



