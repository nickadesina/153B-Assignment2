from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
command_db = {}

@app.route('/chat', methods=['POST'])
def chat():
    chat_text = request.get_json().get('chat', '').strip()
    if chat_text.startswith('/admin'):
        parts = chat_text.split()
        if len(parts) < 2:
            return jsonify({"chat": ""})
        subcommand = parts[1]
        if subcommand == "add" and len(parts) == 4:
            cmd, url = parts[2], parts[3]
            if cmd == "admin":
                return jsonify({"chat": "The /admin command is reserved by the system and cannot be modified"})
            command_db[cmd] = url
            return jsonify({"chat": ""})
        elif subcommand == "update" and len(parts) == 4:
            cmd, url = parts[2], parts[3]
            if cmd == "admin":
                return jsonify({"chat": "The /admin command is reserved by the system and cannot be modified"})
            if cmd in command_db:
                command_db[cmd] = url
            return jsonify({"chat": ""})
        elif subcommand == "delete" and len(parts) == 3:
            cmd = parts[2]
            if cmd == "admin":
                return jsonify({"chat": "The /admin command is reserved by the system and cannot be modified"})
            command_db.pop(cmd, None)
            return jsonify({"chat": ""})
        elif subcommand == "list":
            if not command_db:
                return jsonify({"chat": ""})
            output = "\n".join([f"/{cmd} -> {url}" for cmd, url in command_db.items()])
            return jsonify({"chat": output})
        else:
            return jsonify({"chat": ""})
    if chat_text.startswith('/'):
        parts = chat_text[1:].split(' ', 1)
        command = parts[0]
        message = parts[1] if len(parts) > 1 else ''
        if command in command_db:
            server_url = command_db[command]
            try:
                resp = requests.post(
                    f"{server_url}/chat",
                    json={"chat": message},
                    timeout=5
                )
                return jsonify(resp.json())
            except Exception as e:
                return jsonify({"chat": f"Error contacting server for /{command}: {e}"})
        else:
            return jsonify({"chat": f"The command {command} is not registered."})
    return jsonify({"chat": chat_text})

if __name__ == '__main__':
    app.run(port=5000)