from app import app, db
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.models import User

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    #Create user obj
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
    
        #Incorrect username or pass
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect username or password.")
            return redirect(url_for('login'))
        
        login_user(user,remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '': #ensures netloc is empty (to prevent open redirects)
            next_page = url_for('index')

        return redirect(next_page)
        
    return render_template('login.html',title='Log in',form=form)


@app.route('/cat-images')
@login_required
def cat_pics():
    return render_template('cat_pics.html', title='Cat Pics')
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
