import sqlite3

from Source.AccountHandlerInterface import AccountHandlerInterace

class AccountHandler(AccountHandlerInterace):
    def __init__(self, file_db):
        self.conn = sqlite3.connect(file_db)
        self.users = self.get_all_users()
        self.logged_users = []
        self.create_tables()


    def register_user(self, name, password):
        try: 
            cursor = self.conn.curson()
            cursor.execute(f'''
                            INSERT INTO users (name, password, balance)
                            VALUES ('{name}', '{password}', 0)
                        ''')
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Error, a user with this name already exists")


    def login_user(self, name, password):
        try: 
            cursor = self.conn.curson()
            cursor.execute(f'''
                            SELECT * FROM users
                            WHERE name = {name} and password = {password}')
                        ''')
            
            user = cursor.fetchone()
            if user is None:
                print("Error finding user")
                return False

            return True
        except sqlite3.IntegrityError:
            print("Error, a user with this name and password combination does not exists")


    def get_users(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
                 SELECT id, name, password, balance FROM Users';
                ''')

        users = cursor.fetchall()
        for user in users:
            print(user)

        return users

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
         SELECT name FROM sqlite_master WHERE type='table' AND name='Users';
        ''')

        result = cursor.fetchone()
        if result is None:
            print(f"Table Users dont not exist. Creating it now.")
            cursor.execute('''
            CREATE TABLE Users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                password STRING NOT NULL,
                balance INTEGER
            )
            ''')
            self.conn.commit()
        else:
            print("Table Users already exists")