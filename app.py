from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Store active users and their connections
active_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('current_users', {'users': list(active_users.keys())})

@socketio.on('disconnect')
def handle_disconnect():
    username = active_users.get(request.sid)
    if username:
        del active_users[request.sid]
        emit('user_left', {'username': username}, broadcast=True)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    active_users[request.sid] = username
    emit('user_joined', {'username': username}, broadcast=True)
    emit('current_users', {'users': list(active_users.keys())})

@socketio.on('send_message')
def handle_message(data):
    message = {
        'content': data['content'],
        'username': data['username'],
        'timestamp': data['timestamp'],
        'file': data.get('file')
    }
    emit('receive_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
