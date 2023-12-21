import sqlite3 as sq

async def db_start():
    global db, cur

    db = sq.connect('newtable.db')
    cur = db.cursor()

    cur.execute("CREAT TABLE IF NOT EXISTS review(user_id TEXT PRIMARY KEY, program_version TEXT, date TEXT, time TEXT, review TEXT)")
    db.commit()

async def review_button(user_id):
    user = cur.execute("SELECT 1 FROM review WHERE user_id == '{key'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO review VALUES(?, ?, ?, ?, ?)", (user_id, '', '', '', ''))
        cur.commit()

async def edit_review(user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE review WHERE user_id == '{user_id}'SET user_id = '{}'".format(user_id))