import sqlite3

class AccountHandler:
    def __init__(self, file_db):
        self.conn = sqlite3.connect(file_db)
        self.users = self.get_all_users()
        self.logged_users = []
        self.create_tables()

    def get_all_users(self):
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