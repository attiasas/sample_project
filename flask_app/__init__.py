import os
import sqlite3
from pathlib import Path

from flask import Flask, g

DB_FILENAME = "database.db"








def query_db(query, args=(), one=False, commit=False):
    with sqlite3.connect(DB_FILENAME) as conn:
        conn.set_trace_callback(print)
        # run the query from DB
        cur = conn.cursor().execute(query, args)

        if commit:
            conn.commit()

        return cur.fetchone() if one else cur.fetchall()













def create_app():
    app = Flask(__name__)
    app.secret_key = "abZ1iwoh3ree2mo0Eereireong4baitixaixu4Ee"

    db_path = Path(DB_FILENAME)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(DB_FILENAME)
    create_table_query = """CREATE TABLE IF NOT EXISTS user
    (id INTEGER PRIMARY KEY, username TEXT, password TEXT, access_level INTEGER)"""
    conn.execute(create_table_query)

    insert_admin_query = """INSERT INTO user (id, username, password, access_level)
    VALUES (1, 'admin', 'admin', 0)"""
    conn.execute(insert_admin_query)
    conn.commit()
    conn.close()

    with app.app_context():
        from . import core
        from . import auth
        from . import status
        from . import ui
        from . import users

        app.register_blueprint(core.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(status.bp)
        app.register_blueprint(ui.bp)
        app.register_blueprint(users.bp)
        return app
