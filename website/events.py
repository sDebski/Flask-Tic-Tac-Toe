from .extensions import socketio
from flask_socketio import emit, send, join_room, leave_room, close_room
from flask_login import  login_required, current_user
from flask import request



O = 1
X = 2

class Room():
    room_id = 1
    def __init__(self, player_id, first_name, session_id):
        self.id = Room.room_id
        self.player1_id = player_id
        self.player1_first_name = first_name
        self.session1_id = session_id
        self.player2_id = None
        self.player2_first_name = None
        self.session2_id = None
        self.players = 1
        self.game_state = ['' for el in range(9)]
        Room.room_id += 1
        
    
    def get_players(self):
        return self.players
    
    def player_joined(self, player_id, first_name, session_id):
        self.player2_id = player_id
        self.player2_first_name = first_name
        self.session2_id= session_id
        self.players += 1
        

Rooms = []



@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    
    
@socketio.on("user_join")
def handle_user_join(player_id, first_name, session_id):
    print(f'User {first_name} joined!')
    if len(Rooms) == 0:
        createRoom(player_id, first_name, session_id)
    else:
        for room in Rooms:
            if room.get_players() == 1:
                join_room(room.id)
                room.player_joined(player_id, first_name, session_id)
                print(f'{room.player2_first_name} joined room: {room.id}!')
                send(f'{room.player2_first_name} joined room: {room.id}!', to=room.id)
                data = {'player1_first_name':room.player1_first_name,
                        'player2_first_name':room.player2_first_name,
                        'room_id': room.id}
                emit("players_set", data, to=room.id)
                emit("player_turn", {'my_turn': room.player1_id, 'opponent': room.player2_id}, to=room.id)
                break
        else:
            createRoom(player_id, first_name, session_id)
            
            
def createRoom(player_id, first_name, session_id):
    room = Room(player_id=player_id, first_name=first_name, session_id=session_id)
    Rooms.append(room)
    join_room(room.id)
    print(f'{room.player1_first_name} created and joined room: {room.id}!')
    send(f'{room.player1_first_name} created and joined room: {room.id}!', to=room.id)

        

@socketio.on('user_leave')
def handle_user_leave(player_id, first_name):
    print(f'{first_name} left the room.')
    
    
@socketio.on("move")
def handle_user_move(field_id, sign, user_id, room_id):
    print(f'User {user_id} clicked {field_id} on {room_id}.')
    room = [room for room in Rooms if room.id == room_id][0]
    room.game_state[int(field_id)] = sign
    emit('move_made', {'field_id': field_id, 'sign': sign}, to=room_id)
    
    result = checkIfGameFinished(room, user_id)
    
    if not result:
        if user_id == room.player1_id:
            emit('player_turn', {'my_turn': room.player2_id, 'opponent': room.player1_id}, to=room_id)
        else:
            emit('player_turn', {'my_turn': room.player1_id, 'opponent': room.player2_id}, to=room_id)
    

def checkIfGameFinished(room, user_id):
    print(room.game_state)
    gs = room.game_state

    if ((gs[0] == gs[1] == gs[2] != '') | 
        (gs[3] == gs[4] == gs[5] != '') |
        (gs[6] == gs[7] == gs[8] != '') |
        (gs[0] == gs[3] == gs[6] != '') |
        (gs[1] == gs[4] == gs[7] != '') |
        (gs[2] == gs[5] == gs[8] != '') |
        (gs[0] == gs[4] == gs[8] != '') |
        (gs[2] == gs[4] == gs[6] != '') ):
        
        print('game finished')
        
        data = {
            'winner_id': user_id,
            'p1': room.player1_id,
            'p2': room.player2_id,
            's1': room.session1_id,
            's2': room.session2_id
        }
        emit('game_finished', data, to=room.id)
        return True
    
    if gs.count('') == 0:
        data = {
            'p1': room.player1_id,
            'p2': room.player2_id,
            's1': room.session1_id,
            's2': room.session2_id
        }
        emit('draw', data, to=room.id)
        return True
    
    return False
    
        