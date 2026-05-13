import os
import eventlet

eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(
    app,
    cors_allowed_origins='*',
    async_mode='eventlet'
)

participants = []
messages = []


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def handle_join(username):
    if username and username not in participants:
        participants.append(username)

    emit('participants', participants, broadcast=True)
    emit('messages', messages)


@socketio.on('leave')
def handle_leave(username):
    if username in participants:
        participants.remove(username)

    emit('participants', participants, broadcast=True)


@socketio.on('message')
def handle_message(data):
    if not data:
        return

    username = data.get('username')
    text = data.get('text')
    image = data.get('image')

    if not username:
        return

    if not text and not image:
        return

    message = {
        'username': username,
        'text': text,
        'image': image
    }

    messages.append(message)

    emit('message', message, broadcast=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
