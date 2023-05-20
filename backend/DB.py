import sqlite3 as sq

# Запуск
def main() -> None:
    global db, cur
    db = sq.connect('chat.db')
    cur = db.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS messages(user_name, message_text)')
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, user_name, user_password)')
    db.commit()

# -------------------------------------------------------------------------------
def add_message(user_name: str, message_text: str) -> None:                     #
    cur.execute('INSERT INTO messages Values(?, ?)', (user_name, message_text)) # Недоработано вообще
    db.commit()                                                                 #
# -------------------------------------------------------------------------------

# Добавление пользователя в бд
def add_user(user_name: str, password: str) -> bool | None:
    user = cur.execute(f'SELECT 1 FROM users WHERE user_name== "{user_name}"').fetchone()
    if not user:
        cur.execute('INSERT INTO users (user_name, user_password) Values(?, ?)', (user_name, password))
    else:
        return True
    db.commit()

# Поиск пользователя
def find_user(name: str, password: str) -> tuple | None:
    user = cur.execute(f'SELECT * FROM users WHERE user_name== "{name}"').fetchone()
    if user:
        if user[2] == password:
            return user
    return None

if __name__ == '__main__':
    main()