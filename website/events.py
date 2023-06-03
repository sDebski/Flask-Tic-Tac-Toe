from .extensions import socketio

@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    
    
@socketio.on("user_join")
def handle_user_join(first_name):
    print(f'User {first_name} joined!')