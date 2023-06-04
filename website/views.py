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
            data = request.json
            print('DOTARLEM')
            print(data)
            status = data['status']
            user1 = data['p1']
            user2 = data['p2']
            session1 = data['s1']
            session2 = data['s2']
            
            if data['status'] == 'draw':
                print('dotarlem do draw')
                game = Game(session1_id=session1, user1_id=user1, session2_id=session2, user2_id=user2)
                db.session.add(game)
                db.session.commit()
                flash('Draw game added to database!', category='success')
            else:
                print('dotarlem do wina')
                winner = data['winner_id']
                game = Game(session1_id=session1, user1_id=user1, session2_id=session2, user2_id=user2, result=winner)
                db.session.add(game)
                db.session.commit()
                flash('Won/Lost game added to database!', category='success')
            print('dotarlem do konca.')
    return render_template('game.html', user=current_user, session_id=session.id)