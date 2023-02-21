from flask import Flask, jsonify, make_response
from http import HTTPStatus
application = Flask(__name__)

@application.route("/health/")
def health_check():
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), HTTPStatus.OK)


if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8000)