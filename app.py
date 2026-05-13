from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO, emit
from models import db, Message
from datetime import datetime
from flask_socketio import SocketIO, emit

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")
db.init_app(app)

with app.app_context():
    db.create_all()

participants = []
messages = []
user_sessions = {}
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return {'error': 'Keine Datei'}, 400

    file = request.files['image']

    if file.filename == '':
        return {'error': 'Keine Datei gewählt'}, 400

    filename = secure_filename(file.filename)

    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(path)

    return {
        'url': f'/static/uploads/{filename}'
    }
def index():
    return render_template("chat.html")

@socketio.on("join")
def handle_join(data):
    username = data["username"]
    user_sessions[request.sid] = username

    if username not in participants:
        participants.append(username)

    emit("participants", participants, broadcast=True)

    system_message = {
        "sender": "System",
        "text": f"{username} ist dem Klassenraum beigetreten."
    }

    messages.append(system_message)

    emit("message", system_message, broadcast=True)

@socketio.on("leave")
def handle_leave(data):
    username = data["username"]

    if username in participants:
        participants.remove(username)

    emit("participants", participants, broadcast=True)

    system_message = {
        "sender": "System",
        "text": f"{username} hat den Klassenraum verlassen."
    }

    messages.append(system_message)

    emit("message", system_message, broadcast=True)

@socketio.on("send_message")
def handle_message(data):
    message = {
        "sender": data["sender"],
        "text": data["text"],
        "time": datetime.now().strftime('%H:%M')
    }

    new_message = Message(
        sender=data["sender"],
        text=data["text"]
    )

    db.session.add(new_message)
    db.session.commit()

    emit("message", message, broadcast=True)

@socketio.on("get_state")
def get_state():
    all_messages = Message.query.order_by(Message.created_at.asc()).all()

    history = []

    for msg in all_messages:
        history.append({
            "sender": msg.sender,
            "text": msg.text
        })

    emit("participants", participants)
    emit("message_history", history)

@socketio.on('disconnect')
def handle_disconnect():
    username = user_sessions.get(request.sid)

    if username and username in participants:
        participants.remove(username)

        emit("participants", participants, broadcast=True)

        system_message = {
            "sender": "System",
            "text": f"{username} hat die Verbindung getrennt."
        }

        emit("message", system_message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
