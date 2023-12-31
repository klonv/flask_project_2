
from flask import flash, redirect, render_template, url_for
from app import app

from app.forms import loginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Klonv'}
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
    return render_template('index.pug', title='Home', user=user, posts =posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect( url_for('index'))
    return render_template('login.pug', title='Sign In', form=form)