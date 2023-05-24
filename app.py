from flask import Flask, url_for, request, render_template, session, redirect
from flask_socketio import SocketIO
from flask_login import LoginManager, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Length, DataRequired
from hashlib import md5
from datetime import datetime as dt
import os


# Запуск приложения
app = Flask(__name__)
soketio = SocketIO(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'asklj34lkj453298d7nrjhdo786webtoet786twuigh3ob5736dermax'
db = SQLAlchemy(app)


# Сессия пользователя
class User:
    def create(self, name):
        self.user_ = dict()
        self.user_['name'] = name
        self.user_['password'] = Users().query.get(name).password
        return self
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.user_['name']


# Форма Singup
class FormSingup(FlaskForm):
    name = StringField('Имя: ', validators=[Length(min=5, max=30, message='Пароль должен быть от 5 до 30 символов'), DataRequired('Это обязательное поле')])
    password = PasswordField('Пароль: ', validators=[Length(min=8, max=100), DataRequired('Это обязательное поле')])
    frogt_password = PasswordField('Повторите: ', validators=[Length(min=8, max=100), EqualTo('password', message='Пароли не совпадают'), DataRequired('Это обязательное поле')])
    submit = SubmitField('Sing up')
    


# Все пользователи
class Users(db.Model):
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=False, default=b'')
    
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


@login_manager.user_loader
def load_user(name):
    return User().create(name)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template("chat.html")


@app.route('/signin')
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():                               
    form = FormSingup()
    
    if form.validate_on_submit():
        if not Users.query.get(form.name.data):
            user = Users(name=form.name.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(User().create(form.name.data))
            return redirect('/')
        else:
            return 'Такой пользователь уже есть'
    
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def error_404(_):
    return render_template('404-page.html')
    
if __name__ == '__main__':
    app.run()
