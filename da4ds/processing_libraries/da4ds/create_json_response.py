from flask import jsonify
from flask_socketio import emit

def execute(data_json, name, kind):
    """Creates a json response object that can be handled by the web application"""

    emit('progressLog', {'message': "Creating json response object."})

    json = jsonify({'name': name, 'kind': kind, 'data': str(data_json)})
    return(json)
