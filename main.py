from flask import Flask, url_for, request, session, render_template, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from datetime import datetime as dt
import os
from hashlib import md5


# Сайт и бд
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_db.db'
app.config['SECRET_KEY'] = 'sadkfskfjsfcnlerugytilmsadferuoitcasdewrwtyrtuiuuyhjgbvnvnvx'
log_man = LoginManager(app)
db = SQLAlchemy(app)

# Все пользователи
class Users(db.Model):
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.name


# Для сессии пользователя  
class User:
    def set_info(self, name):
        self.user_ = dict()
        self.user_['name'] = name
        self.user_['password'] = Users.query.get(name).password
        print(self.user_['password'])
        return self
        
    
    def is_authenticated(self):
        return True
    
    
    def is_active(self):
        return True
    
    
    def is_anonymous(self):
        return False
    
    
    def get_id(self):
        return str(self.user_['name'])


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


@log_man.user_loader
def user_load_(name):
    return User().set_info(name)


# Главная страница
@app.route('/')
def home():
    return render_template('home.html')


# Страница регистрации
@app.route('/singup', methods=['GET', 'POST'])
def singup():
    # Перенаправка на свою страничку
    if '_user_id' in session:
        return redirect(f"/home")
    
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if len(name) >= 5 and len(password) >= 8:
            try:
                # Добавление
                ex = Users.query.get(name)
                user = Users(name=name, password=md5(password.encode()).hexdigest())
                db.session.add(user)
                db.session.commit()
                
                # Логин
                user___ = User().set_info(name)
                login_user(user___)
            except:
                # Надо обговорить стили с фронтом
                return 'Такой пользователь уже есть'
                # flach('Такой пользователь уже есть')
        else:
            # Надо обговорить стили с фронтом
            return 'Ошибка длина имени >= 5. Длина пароля >= 8'
            # flach('Ошибка длина имени >= 5. Длина пароля >= 8')
        return redirect('/')
    
    return render_template('authorisation.html')


# Страница Авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Перенаправка на свою страничку
    if '_user_id' in session:
        return redirect(f"/home")
    
    # Проверка данных
    if request.method == 'POST':
        name = request.form['name']
        password = md5(request.form['password'].encode()).hexdigest()
        user = User().set_info(name)

        if user.user_['password'] == password:
            login_user(user)
            return redirect(f'/home/{name}')
        else:
            # Надо обговорить стили с фронтом
            return 'Ошибка авторизации'
            # flach('Ошибка авторизации')
    return render_template('registration.html')


# Страница чата для пользователя
@app.route('/chat', methods=['GET', 'POST'])
@app.route('/<name>/chat', methods=['GET', 'POST'])
@login_required
def chat(name: str = None):
    
    # Данные об пользователе (надо обговорить с фронтом)
    user = ...

    # Переадресация для понимания пользователем
    if name is None:
        return redirect(f"/{session['_user_id']}/chat")
    
    # Добавление сообщения
    if request.method == 'POST':
        message = Message(from_user=name, text=request.form['message'])
        db.session.add(message)
        db.session.commit()
        return redirect(f"/{name}/chat")
    
    # Отправка сообщений чата через Jinja
    messages = Message.query.all()
    return render_template('Chat2.html', messages=messages) # render_template('Chat.html', user=user, messages=messages)


# Страничка пользователя
@app.route('/home')
@app.route('/home/<name>')
@login_required
def user_home(name: str = None):
    if name is None:
        redirect(f"/home/{session['_user_id']}")
        
    # Данные об пользователе (надо обговорить с фронтом)
    user = ...
    return 'Вы в настройках аккаунта' # render_template('....html', user=user)
            


# Обработка 404
@app.errorhandler(404)
def error_404(_):
    
    # Страничка ошибки (надо обговорить с фронтом)
    return 'Похоже, вы нетуда попали'


@app.errorhandler(401)
def error_401(_):
    
    # Страничка ошибки (надо обговорить с фронтом)
    return 'Нужно зарегестрироватся'


if __name__ == '__main__':
    app.run(port=1231, debug=True)