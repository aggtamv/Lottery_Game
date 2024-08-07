from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    name = current_user.username if current_user.is_authenticated else 'Guest'
    return render_template('layout.html', name = name)




