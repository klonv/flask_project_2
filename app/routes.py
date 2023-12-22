
from flask import flash, redirect, render_template, url_for, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import loginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa



@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Klonv'}
    posts = [
        {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
        },
        {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
        }
    ]
    # return render_template('index.pug', title='Home', user=user, posts =posts)
    return render_template('index.pug', title='Home', posts =posts)

# поддельный вход, который только что выдал flash()сообщение
"""@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect( url_for('index'))
    return render_template('login.pug', title='Sign In', form=form)"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Неверное Имя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.pug', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))