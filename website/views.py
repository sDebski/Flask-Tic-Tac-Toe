from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  login_required, current_user
from .models import *


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # check if there is an active session
    session = Session.query.filter_by(user_id=current_user.id, finished=False).first()
    if session:
        flash('You already have a session.', category='error')
        return redirect(url_for('.game'))
    
    if request.method =='POST':
        new_session = Session(user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()
        flash('Session created!', category='success')
        return redirect(url_for('.game'))
        
    return render_template('home.html', user=current_user, session_on=True)

@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    session = Session.query.filter_by(user_id=current_user.id, finished=False).first()
    if not session:
        flash('You do not have active session.', category='error')
        print(session.user_id)
        print(session.user_id, session.date, session.points, session.finished)
    else:
        if request.method=='POST':
            print('DOTARLEM')
            #look for an open game
            game = Game.query.filter_by(user2_id=None, session2_id=None).first()
            if game:
                flash('Joining the game!', category='success')
                game.session2_id=session.id
                game.user2_id=current_user.id
                db.session.add(game)
                db.session.commit()
                return {'new': 'false', 'game_id': game.id}
            else:
                flash('Waiting for an opponent!', category='success')
                new_game = Game(session1_id=session.id, user1_id=current_user.id)
                db.session.add(new_game)
                db.session.commit()
                print(new_game)
                return {'new': 'true', 'game_id': game.id}
            
    return render_template('game.html', user=current_user)