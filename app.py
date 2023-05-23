from flask import Flask, request, render_template
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import datetime as dt
import os


# Запуск приложения
app = Flask(__name__)
soketio = SocketIO(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Все пользователи
class Users(db.Model):
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=False)
    
    def __repr__(self):
        return '<Users %r>' % self.name


# Сообщения
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=dt.utcnow())

    def __repr__(self):
        return '<Message %r>' % self.name


# Создание бд если нету
if not os.path.exists(f'instance/{app.config["SQLALCHEMY_DATABASE_URI"]}'):
    with app.app_context():
        db.create_all()

# Дальше вообще недоделано

@login_manager.user_loader
def load_user(user_id):
    user = request.form['name']
    user = request.form['password']
    return user

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/chat')
def chat():
    return render_template("chat.html")


@app.route('/signin')
def signin():
    return render_template("signin.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")
    
if __name__ == '__main__':
    app.run()
