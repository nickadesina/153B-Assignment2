from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nickadesina:KonataIzumi1#@localhost:5432/assignment2DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
default_reserved_command = "admin"

class Command(db.Model):
    __tablename__ = 'commands'
    command = db.Column(db.String, primary_key=True)
    server_url = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

def add_command(command, server_url):
    if command == default_reserved_command:
        return False, "The /admin command is reserved by the system and cannot be modified"
    if Command.query.get(command):
        return False, "Command already exists"
    db.session.add(Command(command=command, server_url=server_url))
    db.session.commit()
    return True, ""

def update_command(command, server_url):
    if command == default_reserved_command:
        return False, "The /admin command is reserved by the system and cannot be modified"
    cmd = Command.query.get(command)
    if not cmd:
        return False, "Command does not exist"
    cmd.server_url = server_url
    db.session.commit()
    return True, ""

def delete_command(command):
    if command == default_reserved_command:
        return False, "The /admin command is reserved by the system and cannot be modified"
    cmd = Command.query.get(command)
    if not cmd:
        return False, "Command does not exist"
    db.session.delete(cmd)
    db.session.commit()
    return True, ""

def list_commands():
    return Command.query.all()

def get_command_url(command):
    cmd = Command.query.get(command)
    return cmd.server_url if cmd else None

@app.route('/chat', methods=['POST'])
def chat():
    chat_text = request.get_json().get('chat', '').strip()
    if chat_text.startswith('/admin'):
        parts = chat_text.split()
        if len(parts) < 2:
            return jsonify({"chat": "Invalid /admin command."})
        subcommand = parts[1]
        # /admin add [command] [server_url]
        if subcommand == 'add':
            if len(parts) != 4:
                return jsonify({"chat": "Usage: /admin add [command] [server_url]"})
            command, server_url = parts[2], parts[3]
            success, msg = add_command(command, server_url)
            if not success:
                return jsonify({"chat": msg})
            return ('', 204)  # No content
        # /admin update [command] [server_url]
        elif subcommand == 'update':
            if len(parts) != 4:
                return jsonify({"chat": "Usage: /admin update [command] [server_url]"})
            command, server_url = parts[2], parts[3]
            success, msg = update_command(command, server_url)
            if not success:
                return jsonify({"chat": msg})
            return ('', 204)
        # /admin delete [command]
        elif subcommand == 'delete':
            if len(parts) != 3:
                return jsonify({"chat": "Usage: /admin delete [command]"})
            command = parts[2]
            success, msg = delete_command(command)
            if not success:
                return jsonify({"chat": msg})
            return ('', 204)
        # /admin list
        elif subcommand == 'list':
            cmds = list_commands()
            if not cmds:
                return ('', 204)
            result = "\n".join([f"/{cmd.command} -> {cmd.server_url}" for cmd in cmds])
            return jsonify({"chat": result})
        else:
            return jsonify({"chat": f"Unknown /admin subcommand: {subcommand}"})
    # Handle other commands
    elif chat_text.startswith('/'):
        parts = chat_text.split(maxsplit=1)
        command = parts[0][1:]
        message = parts[1] if len(parts) > 1 else ''
        server_url = get_command_url(command)
        if server_url:
            try:
                resp = requests.post(
                    f"{server_url}/chat",
                    json={"chat": message},
                    timeout=5
                )
                return jsonify(resp.json())
            except Exception as e:
                return jsonify({"chat": f"Error contacting server for /{command}"})
        else:
            return jsonify({"chat": f"The command {command} is not registered."})
    # No command, just return the message
    return jsonify({"chat": chat_text})

if __name__ == '__main__':
    app.run(port=5000)