from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import EqualTo, Length, DataRequired
from datetime import datetime as dt
import os


def init_(app: Flask, db: SQLAlchemy):
    # Все пользователи
    class Users_(db.Model):
        name = db.Column(db.String, primary_key=True)
        password = db.Column(db.String, nullable=False)
        avatar = db.Column(db.LargeBinary, nullable=False, default=b'')
            
        def __repr__(self):
            return '<Users %r>' % self.name
    
    
    # Сообщения
    class Message_(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        from_user = db.Column(db.String, nullable=False)
        text = db.Column(db.String, nullable=False)
        datetime = db.Column(db.DateTime, default=dt.utcnow())

        def __repr__(self):
            return '<Message %r>' % self.name

    
    # Сессия пользователя
    class User_:
        def create(self, name):
            self.user_ = dict()
            self.user_['name'] = name
            self.user_['password'] = Users_().query.get(name).password
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
    class FormSingup_(FlaskForm):
        name = StringField('Имя: ', validators=[Length(min=5, max=30, message='Пароль должен быть от 5 до 30 символов'), DataRequired('Это обязательное поле')])
        password = PasswordField('Пароль: ', validators=[Length(min=8, max=100), DataRequired('Это обязательное поле')])
        frogt_password = PasswordField('Повторите: ', validators=[Length(min=8, max=100), EqualTo('password', message='Пароли не совпадают'), DataRequired('Это обязательное поле')])
        submit = SubmitField('Sing up')
    

    # Форма Singin
    class FormLogin_(FlaskForm):
        name = StringField('Имя: ', validators=[Length(min=5, max=30), DataRequired('Это обязательное поле')])
        password = PasswordField('Пароль: ', validators=[Length(min=8, max=100), DataRequired('Это обязательное поле')])
        remember = BooleanField('Запомнить? ', default=False)
        submit = SubmitField('Login')
    
    
    # Создание бд если нету
    if not os.path.exists(f'instance/{app.config["SQLALCHEMY_DATABASE_URI"]}'):
        with app.app_context():
            db.create_all()
    
    
    # global Users, Message, User, FormSingup, FormLogin
    return Users_, Message_, User_, FormSingup_, FormLogin_