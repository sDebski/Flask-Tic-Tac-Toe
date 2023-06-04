from .extensions import socketio
from flask_socketio import emit, send, join_room, leave_room, close_room
from flask_login import  login_required, current_user
from flask import request



O = 1
X = 2

class Room():
    room_id = 1
    def __init__(self, player_id, first_name):
        self.id = Room.room_id
        self.player1_id = player_id
        self.player1_first_name = first_name
        self.player2_id = None
        self.player2_first_name = None
        self.players = 1
        self.game_state = ['' for el in range(9)]
        Room.room_id += 1
        
    
    def get_players(self):
        return self.players
    
    def player_joined(self, player_id, first_name):
        self.player2_id = player_id
        self.player2_first_name = first_name
        self.players += 1
        

Rooms = []



@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    
    
@socketio.on("user_join")
def handle_user_join(player_id, first_name):
    print(f'User {first_name} joined!')
    if len(Rooms) == 0:
        createRoom(player_id, first_name)
    else:
        for room in Rooms:
            if room.get_players() == 1:
                join_room(room.id)
                room.player_joined(player_id, first_name)
                print(f'{room.player2_first_name} joined room: {room.id}!')
                send(f'{room.player2_first_name} joined room: {room.id}!', to=room.id)
                data = {'player1_first_name':room.player1_first_name,
                        'player2_first_name':room.player2_first_name}
                emit("players_set", data, to=room.id)
                emit("player_turn", {'player1_id': room.player1_id}, to=room.id)
                break
        else:
            createRoom(player_id, first_name)
            
            
def createRoom(player_id, first_name):
    room = Room(player_id=player_id, first_name=first_name)
    Rooms.append(room)
    join_room(room.id)
    print(f'{room.player1_first_name} created and joined room: {room.id}!')
    send(f'{room.player1_first_name} created and joined room: {room.id}!', to=room.id)

        

@socketio.on('user_leave')
def handle_user_leave(player_id, first_name):
    leave_room
    
    
@socketio.on("move")
def handle_user_move(value):
    print(f'User clicked {value}.')
    emit('Move', {'value: {value}'}, broadcast=True)
    