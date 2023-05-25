from flask import Flask, url_for, request, render_template, session, redirect
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import datetime as dt
from functools import partial
import os

from classes import init_

# Запуск приложения
app = Flask(__name__)
soketio = SocketIO(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'asklj34lkj453298d7nrjhdo786webtoet786twuigh3ob5736dermax'
socetio = SocketIO(app)
db = SQLAlchemy(app)


# Инициализация
Users, Message, User, FormSignup, FormLogin, FormChat = init_(app, db)
links1 = {'/signup': 'Sign up', '/login': 'Log in'}
links2 = {'/logout': 'Log out'}


####################################################################################
old_rt = render_template                                                           # Гениально, да?
def render_template(*args, **kwargs):                                              # Но partial НЕ работает
    return old_rt(*args, **kwargs, links_=[links1, links2]['_user_id' in session]) # Так что такой декоратор
####################################################################################


# Загрузка пользователя
@login_manager.user_loader
def load_user(name):
    return User().create(name)


# Главная страница
@app.route('/')
def index():
    
    return render_template("index.html")


# Про нас
@app.route('/about')
def about():
    return render_template("about.html")


# Чат
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    messages = Message().query.all()
    return render_template("chat.html", messages=messages)

@socetio.on('message')
def message_handler(message_):
    message = Message(text=message_, from_user= session['_user_id'])
    db.session.add(message)
    db.session.commit()
    emit('response', message_, broadcast=True)


# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    
    if form.validate_on_submit():
        user = Users().query.get(form.name.data)
        
        if user and user.password == md5(form.password.data.encode()).hexdigest():
            login_user(User().create(form.name.data), remember=form.remember.data)
            return redirect('/')
        
        return 'Некоректные данные'
    return render_template("login.html", form=form)


# Регистрация
@app.route('/signup', methods=['GET', 'POST'])
def signup():                               
    form = FormSignup()
    
    if form.validate_on_submit():
        if not Users.query.get(form.name.data):
            user = Users(name=form.name.data, password=md5(form.password.data.encode()).hexdigest())
            db.session.add(user)
            db.session.commit()
            login_user(User().create(form.name.data))
            return redirect('/')
        
        return 'Такой пользователь уже есть'
    
    return render_template("signup.html", form=form)


# Выход с профиля
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# Обработка 404
@app.errorhandler(404)
def error_404(_):
    return render_template('404-page.html')


if __name__ == '__main__':
    socetio.run(app)