from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    draw_numbers = db.relationship('Draw_stats', back_populates='user', cascade='all, delete-orphan')

    def max_correct_guesses(self):

        max_correct = 0
        max_date = None
        for draw_stat in self.draw_numbers:
            guessed_numbers = set(draw_stat.numbers_guess.split(','))
            drawn_numbers = set(draw_stat.numbers_draw.split(','))
            correct_guesses = len(guessed_numbers.intersection(drawn_numbers))
            if correct_guesses > max_correct:
                max_correct = correct_guesses
                max_date = draw_stat.draw_datetime
        return max_correct, max_date


class Draw_stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    numbers_guess = db.Column(db.String(50), nullable=False)  # Storing comma-separated numbers
    numbers_draw = db.Column(db.String(50), nullable=False, default='')
    draw_datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.relationship('User', back_populates='draw_numbers')

def delete_null_rows():
    # Example: Delete rows where both 'numbers_guess' and 'numbers_draw' are NULL
    Draw_stats.query.filter(Draw_stats.numbers_guess == None, Draw_stats.numbers_draw == None).delete()
    db.session.commit() 


