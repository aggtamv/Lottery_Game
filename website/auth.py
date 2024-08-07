from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from .models import User, Draw_stats
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import smtplib


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                session["user_id"] = user.id  # Store user ID in session
                return redirect(url_for('auth.draw'))
            else:
                flash('Password is incorrect', category= 'error')
        else:
            flash('Email does not exist!', category='error')
            
    return render_template("login.html", user=current_user)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created', category='success')
            return redirect(url_for('auth.login'))
        
    username = current_user.username if current_user.is_authenticated else None
    return render_template('register.html', username=username)

@auth.route("/draw", methods=['GET', 'POST'])
@login_required
def draw():
    data = Draw_stats.query.all()
    if request.method == 'POST':
            numbers_guess = request.form.get('selected_numbers')
            numbers_draw = request.form.get('lottery_numbers')
            print(f"Numbers guessed: {numbers_guess}, Numbers drawn: {numbers_draw}")

            if numbers_guess and numbers_draw:
                # Print to debug if user is properly fetched and attached to the session
                user = User.query.get(current_user.id)
                print(f"User: {user}")

                # Create and add a new entry to the database
                new_entry = Draw_stats(user_id=user.id, numbers_guess=numbers_guess, numbers_draw=numbers_draw)
                db.session.add(new_entry)
                db.session.commit()
                flash('Numbers saved successfully!', category='success')
            else:
                flash('No numbers selected!', category='error')
    return render_template("draw.html", username=current_user, data = data)

@auth.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    print("Logout route hit")
    logout_user()
    flash("You have been logged out.", category='success')
    return redirect(url_for("views.home"))


@auth.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.all()
    leaderboard_data = []

    for user in users:
        max_correct_guesses, max_correct_date = user.max_correct_guesses()
        formatted_date = max_correct_date.strftime('%Y-%m-%d') if max_correct_date else None
        leaderboard_data.append({
            'username': user.username,
            'max_correct_guesses': max_correct_guesses,
            'max_correct_date': formatted_date
        })

    # Sort the data by max_correct_guesses in descending order
    sorted_leaderboard = sorted(leaderboard_data, key=lambda x: x['max_correct_guesses'], reverse=True)

    # Add rank to each user
    for index, data in enumerate(sorted_leaderboard, start=1):
        data['rank'] = index
    
    # Assuming 'current_user' is a logged-in user
    recent_draws = Draw_stats.query.filter_by(user_id=current_user.id) \
                                   .order_by(Draw_stats.draw_datetime.desc()) \
                                   .limit(5) \
                                   .all()

    return render_template('leaderboard.html', leaderboard_data=sorted_leaderboard, recent_draws = recent_draws)