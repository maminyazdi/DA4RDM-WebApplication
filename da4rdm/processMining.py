import os
from os.path import isfile, join
from flask import (
    Blueprint, render_template,request
)

bp = Blueprint('blueprints/main', __name__)

process_mining_bp = Blueprint('blueprints/process_mining', __name__, template_folder='templates', static_folder='static')

@process_mining_bp.route('/')
def process_mining():
    return render_template('process_mining/process_mining.html')

@process_mining_bp.route('/process_discovery')
def process_discovery():
    # get all available discovery algorithms
    discovery_algorithm_labels = {"alpha_miner": "Alpha Miner",
                                  "directly_follows_graph": "Directly Follows Graph",
                                  "heuristic_miner": "Heuristic Miner",
                                  "inductive_miner": "Inductive Miner"}

    discovery_algorithm_path = './da4rdm/api/process_mining/discovery_algorithms/'
    files = [file for file in os.listdir(discovery_algorithm_path)if isfile(join(discovery_algorithm_path, file))]
    discovery_algorithms = [str(x)[:-3] for x in files if x != "__init__.py"]

    return render_template('process_mining/process_discovery.html', discovery_algorithms=discovery_algorithms, discovery_algorithm_labels=discovery_algorithm_labels)
