from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('chat', '')
    if message.startswith('/'):
        parts = message[1:].split(' ', 1)
        command = parts[0]
        msg_part = parts[1] if len(parts) > 1 else ''
        response = f"{command}: {msg_part}"
    else:
        response = f"None: {message}"
    return jsonify({"chat": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)