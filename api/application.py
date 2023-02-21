from flask import Flask, jsonify, make_response
application = Flask(__name__)

@application.route("/health/")
def health_check():
	# return 'ok', 200
	resp = {'status' : 'ok'}
	return make_response(jsonify(resp), 200)
	# return jsonify(resp)
    # return make_response(jsonify(), 200)


if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8000)