from flask import Flask, request, render_template
from brute_force import register_failed_attempt, blocked_ips
import sqlite3

app = Flask(__name__)

def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None


@app.before_request
def check_blocklist():
    user_ip = request.remote_addr
    if user_ip in blocked_ips:
        return "Your IP is blocked due to too many failed attempts.", 403


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    user_ip = request.remote_addr
    username = request.form['username']
    password = request.form['password']

    if validate_user(username, password):
        return f"Welcome {username}! Your IP: {user_ip}"

    # Wrong login → count brute-force attempts
    register_failed_attempt(user_ip)
    return render_template("login.html", msg="Invalid credentials")


app.run(host="0.0.0.0", port=5000, debug=True)
