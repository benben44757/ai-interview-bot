from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/interview', methods=['GET'])
def get_interview():
    return jsonify({'message': 'Welcome to the AI Interview Bot!'}), 200

@app.route('/interview', methods=['POST'])
def post_interview():
    data = request.json
    # Process interview data
    return jsonify({'message': 'Interview data received!', 'data': data}), 201

if __name__ == '__main__':
    app.run(debug=True)