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
    if session:
        flash('You already have a session.', category='error')
        print(session.user_id)
        print(session.user_id, session.date, session.points, session.finished)
    return render_template('game.html', user=current_user)