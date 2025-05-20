from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    message = request.get_json().get('chat', '')
    return jsonify({"chat": message + "¯\_(ツ)_/¯"})

if __name__ == '__main__':
    app.run(port=5001)
