from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")

participants = []
messages = []

@app.route("/")
def index():
    return render_template("chat.html")

@socketio.on("join")
def handle_join(data):
    username = data["username"]

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
        "text": data["text"]
    }

    messages.append(message)

    emit("message", message, broadcast=True)

@socketio.on("get_state")
def get_state():
    emit("participants", participants)
    emit("message_history", messages)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
