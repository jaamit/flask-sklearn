from flask import Flask, jsonify, make_response, request
from http import HTTPStatus
from models import create_classifier_model, fetch_model, train_the_model
from db import create_table, drop_table

application = Flask(__name__)
create_table()
# drop_table()

@application.route("/health/")
def health_check():
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), HTTPStatus.OK)

@application.post("/models/")
def create_model():
    request_data = request.get_json()
    unique_id = create_classifier_model(request_data)
    resp = {'id' : unique_id}
    return make_response(jsonify(resp), HTTPStatus.OK)

@application.get("/models/<int:model_id>/")
def get_model(model_id):
	print(model_id)
	model_metadata = fetch_model(model_id)
	return make_response(jsonify(model_metadata), HTTPStatus.OK)

@application.post("/models/<int:model_id>/train/")
def train_model(model_id):
	request_data = request.get_json()
	train_the_model(model_id, request_data)
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), HTTPStatus.OK)

# @application.get("/models/<int:model_id>/predict/?x=<str:base64(x)>")
# def predict():
# 	resp = {'status' : 'ok'}
# 	return make_response(jsonify(resp), HTTPStatus.OK)
	 
@application.get("/models/")
def most_trained_model_score():
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), HTTPStatus.OK)

@application.get("/models/groups/")
def model_groups():
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), HTTPStatus.OK)




if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8000)