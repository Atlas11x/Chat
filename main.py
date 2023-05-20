from flask import Flask, request
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask import render_template
from hashlib import md5
import backend.DB as db

# Пользователь
class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password_h = md5(password.encode()).hexdigest()
        
    def save_user(self) -> str:
        if db.add_user(self.name, self.password_h):
            return 'Такой пользователь уже есть'
        else:
            return 'Пользователь создан'
        
    @staticmethod
    def find_user(name: str, password: str):
        user = db.find_user(name, md5(password.encode()).hexdigest())
        if user:
            return User(*user[1:])
        return False
    
# Запуск приложения
app = Flask(__name__)
soketio = SocketIO(app)
login_manager = LoginManager(app)

# Дальше вообще недоделано

@login_manager.user_loader
def load_user(user_id):
    user = request.form['name']
    user = request.form['password']
    return user

@app.route('/')
def start():
    return render_template('html/index.html')


# @app.route('/login', methods=['POST'])
def start():
    
    name = ...
    return render_template('html/index.html')


@app.route('/chat')
def chat():
    return render_template('html/Chat.html')

@soketio.on('message')
def message_handler(data):
    db.add_message(data.user, data.text)
    print(data)
    soketio.emit('message', data, broadcast=True)
    
    
    
if __name__ == '__main__':
    db.main()
    soketio.run(app)