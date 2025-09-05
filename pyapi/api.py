import os
import psycopg2
import time
import redis
from flask import Flask, jsonify, request 

app = Flask(__name__)

REDIS_HOST =os.environ.get("REDIS_HOST")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

cache = redis.Redis(host=REDIS_HOST, port=6379)

'''
def wait_for_db():
    for i in range(10):
        try:
            conn = get_db_connection()
            conn.close()
            print("Database is ready")
            return
        except psycopg2.OperationalError as e:
            print(f"Database not ready, retrying ({i+1}/10)...")
            time.sleep(3)
    raise Exception("Database not available after 10 retries")
'''

def get_msg_count():
    cached = cache.get("message_count")
    if cached is not None:
        return int(cached)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM messages")
    msg_count = cur.fetchone()[0]
    conn.close()
    cache.set("message_count", msg_count)
    return msg_count

def add_msg_count():
    retries = 3
    while True:
        try:
            return cache.incr('message_count')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)           

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=5432
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, msg VARCHAR , created_at TIMESTAMP DEFAULT NOW());")
    conn.commit()
    cur.close()
    conn.close()

@app.route("/messages" , methods=["GET"])
def GET():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT msg,created_at FROM messages;")
    rows = cur.fetchall()
    messages=[{"text": row[0] ,"created_at":row[1]} for row in rows]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(messages)

@app.route("/messages" , methods=["POST"])
def POST():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    msg_txt=data["text"]
    cur.execute("INSERT INTO messages (msg) VALUES (%s);",(msg_txt,))
    add_msg_count()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "ok", "msg": msg_txt}), 201

@app.route("/count")
def count():
    count = get_msg_count()
    return "THERE IS {} MESSAGES IN DB!".format(count)


if __name__ == "__main__":
    #wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=3000, debug=True)
