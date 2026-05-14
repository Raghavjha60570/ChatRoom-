from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active users
users = {}
rooms = {}
messages_file = 'messages.json'

# Load existing messages from file
def load_messages():
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

# Save messages to file
def save_messages(data):
    with open(messages_file, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize messages storage
all_messages = load_messages()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('response', {'data': 'Connected to server'})

@socketio.on('join')
def on_join(data):
    username = data['username'].strip()
    room = data['room'].strip()
    
    if not username or not room:
        emit('error', {'message': 'Username and room are required'})
        return
    
    join_room(room)
    users[request.sid] = {'username': username, 'room': room}
    
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(username)
    
    # Send previous messages in this room
    if room in all_messages:
        for msg in all_messages[room]:
            emit('message', msg)
    
    # Notify everyone
    system_msg = {
        'username': 'System',
        'message': f'{username} joined the chat',
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': 'system'
    }
    emit('message', system_msg, room=room)
    
    emit('user_list', {'users': rooms.get(room, [])}, room=room)
    print(f'{username} joined room: {room}')

@socketio.on('send_message')
def handle_message(data):
    if request.sid not in users:
        emit('error', {'message': 'Not connected'})
        return
    
    user_info = users[request.sid]
    room = user_info['room']
    
    message_obj = {
        'username': user_info['username'],
        'message': data['message'],
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': 'user'
    }
    
    # Save message to storage
    if room not in all_messages:
        all_messages[room] = []
    all_messages[room].append(message_obj)
    save_messages(all_messages)
    
    # Broadcast to all users in room
    emit('message', message_obj, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        user_info = users[request.sid]
        room = user_info['room']
        username = user_info['username']
        
        if room in rooms:
            rooms[room].remove(username)
            if not rooms[room]:
                del rooms[room]
        
        emit('message', {
            'username': 'System',
            'message': f'{username} left the chat',
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'system'
        }, room=room)
        
        emit('user_list', {'users': rooms.get(room, [])}, room=room)
        del users[request.sid]
    
    print(f'Client disconnected: {request.sid}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
