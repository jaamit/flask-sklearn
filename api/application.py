from flask import Flask, jsonify, make_response, request
from http import HTTPStatus
from models import create_classifier_model

application = Flask(__name__)

@application.route("/health/")
def health_check():
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), HTTPStatus.OK)

# @application.route("/models/", methods = ['POST'])
@application.post("/models/")
def create_model():
    request_data = request.get_json()
    resp = create_classifier_model(request_data)
    resp = {'status' : 'ok'}
    return make_response(jsonify(resp), HTTPStatus.OK)
	

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8000)