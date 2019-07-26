from flask import Flask
from flask import request, jsonify

import rate_service
from invalid_data import InvalidData

app = Flask(__name__)


@app.route('/rates', methods=['POST'])
def save_rate():
    payload = request.get_json()
    rate_service.save_rate(payload)
    return 'Saved Rate!'


@app.route('/rates', methods=['GET'])
def get_rate():
    to_datestring = request.args.get('to')
    from_datestring = request.args.get('from')
    rate = rate_service.get_rate(from_datestring, to_datestring)
    return str(rate)


@app.errorhandler(InvalidData)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run()
