from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from ..models.models import *
import datetime
from sqlalchemy import or_


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    session_on = False
    # check if there is an active session
    session = Session.query.filter_by(user_id=current_user.id, finished=False).first()
    if session:
        # flash('You already have a session.', category='error')
        session_on = True

    if request.method == "POST":
        new_session = Session(user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()
        flash("Session created!", category="success")
        return redirect(url_for("views.game"))

    return render_template("home.html", user=current_user, session_on=session_on)


@views.route("/game", methods=["GET", "POST"])
@login_required
def game():
    session = Session.query.filter_by(user_id=current_user.id, finished=False).first()
    if session == None:
        flash("You do not have active session.", category="error")
        return redirect(url_for("views.home"))
    else:
        balance = session.points
        if request.method == "POST":
            data = request.json
            status = data["status"]
            user1 = data["p1"]
            user2 = data["p2"]
            session1 = data["s1"]
            session2 = data["s2"]

            if data["status"] == "draw":
                game = Game(
                    session1_id=session1,
                    user1_id=user1,
                    session2_id=session2,
                    user2_id=user2,
                )
                db.session.add(game)
                db.session.commit()
                flash("Draw game added to database!", category="success")
            if data["status"] == "won":
                winner = data["winner_id"]
                # check credits balance
                if winner == str(current_user.id):
                    new_balance = balance + 4
                    game = Game(
                        session1_id=session1,
                        user1_id=user1,
                        session2_id=session2,
                        user2_id=user2,
                        result=winner,
                    )
                    db.session.add(game)
                    db.session.commit()
                else:
                    new_balance = balance - 3
                session.points = new_balance
                balance = new_balance

                if new_balance < 3:
                    session.finished = True

                db.session.add(session)
                db.session.commit()
    return render_template(
        "game.html", user=current_user, session_id=session.id, credits=balance
    )


@views.route("/statistics", methods=["GET"])
@login_required
def statistics():
    my_id = current_user.id
    games = list(Game.query.filter((Game.user1_id == my_id) | (Game.user2_id == my_id)))

    result = games
    today = datetime.datetime.now().date()
    print(today)
    result = [game for game in result if game.date.date() == today]

    return render_template("statistics.html", games=result, user=current_user)
