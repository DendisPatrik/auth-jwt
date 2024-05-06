from flask import Flask, jsonify, request

from auth_utility import token_required, AuthUtility

app = Flask(__name__)
SECRET_KEY = 'nejaky nahodny retazaec'


@app.route('/generate-token', methods=['POST'])
def login():
    username = request.json.get('username')
    return jsonify({'token': AuthUtility.generate_token(username)})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Protected'})


@app.route('/opened')
def opened():
    return jsonify({'message': 'Opened'})

if __name__ == '__main__':
    app.run()
