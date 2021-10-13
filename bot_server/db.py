import sqlite3


class DBHelper:

    def __init__(self, dbname="whats_tracker.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT , user_name text, online_status text, active_time text)"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_user(self, user_name, online_status, active_time):
        stmt = "INSERT INTO users (user_name, online_status, active_time) VALUES (?, ?, ?)"
        args = (user_name, online_status, active_time)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_user(self, chat_id):
        stmt = "DELETE FROM users WHERE id = (?)"
        args = (chat_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

   