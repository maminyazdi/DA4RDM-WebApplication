##ConformanceChecking ..added by Mrunmai
from flask import (
	Blueprint, render_template
)

bp = Blueprint('blueprints/main', __name__)

conformance_checking_bp = Blueprint('blueprints/conformance_checking',__name__, template_folder='templates', static_folder='static')

@conformance_checking_bp.route('/')
def conformance_checking():
	return render_template('conformance_checking/conformance_checking.html')