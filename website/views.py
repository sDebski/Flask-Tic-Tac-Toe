from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  login_required, current_user
from .models import *


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    session_on = False
    # check if there is an active session
    session = Session.query.filter_by(user_id=current_user.id, finished=False).first()
    if session:
        #flash('You already have a session.', category='error')
        session_on = True
    
    if request.method =='POST':
        new_session = Session(user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()
        flash('Session created!', category='success')
        return redirect(url_for('views.game'))
        
    return render_template('home.html', user=current_user, session_on=session_on)

@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    session = Session.query.filter_by(user_id=current_user.id, finished=False).first()
    if session == None:
        flash('You do not have active session.', category='error')
        return redirect(url_for('views.home'))
    else:
        balance = session.points
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
            if data['status'] == 'won':
                print('dotarlem do wina')
                winner = data['winner_id']
                print(current_user.id, winner, ' check winner')
                print(winner == current_user.id)
                #check credits balance
                if winner == str(current_user.id):
                    print('zwiekszam bilans graczowi ', current_user.first_name)
                    new_balance = balance + 4
                    game = Game(session1_id=session1, user1_id=user1, session2_id=session2, user2_id=user2, result=winner)
                    db.session.add(game)
                    db.session.commit()
                else:
                    print('zmniejszam bilans graczowi ', current_user.first_name)
                    new_balance = balance - 3
                session.points = new_balance
                balance = new_balance
    
                if new_balance < 3:
                    session.finished = True
                    
                db.session.add(session)
                db.session.commit()
                print(new_balance)

                return redirect(url_for('.home'))
            print('dotarlem do konca.')
    return render_template('game.html', user=current_user, session_id=session.id, credits=balance)