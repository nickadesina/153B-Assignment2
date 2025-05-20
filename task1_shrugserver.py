from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('chat', '')
    response = message + "¯\_(ツ)_/¯"
    return jsonify({"chat": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)