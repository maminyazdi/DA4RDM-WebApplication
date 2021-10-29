##ConformanceChecking ..added by Mrunmai
import os
from os.path import isfile, join
from flask import (
	Blueprint, render_template,request
)

import da4rdm.api.api as api
from da4rdm.api import user_session

bp = Blueprint('blueprints/main', __name__)

conformance_checking_bp = Blueprint('blueprints/conformance_checking',__name__, template_folder='templates', static_folder='static')

@conformance_checking_bp.route('/')
def conformance_checking():
	#Added for displaying unique operation values on Conformance Page
	operationList = api.get_unique_operations()
	print('operationList.args',operationList)

	return render_template('conformance_checking/conformance_checking.html',operation_list=operationList)

