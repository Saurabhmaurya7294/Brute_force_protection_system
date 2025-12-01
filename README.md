# 🛡️ Brute-Force Protection System (Web Login + IP Blocking)

A Python-based **web login system** with **automatic brute-force attack prevention**. It detects repeated failed login attempts and blocks the attacker’s IP using application-level blocking and system-level firewall (iptables).

---

## 🚀 Features

* **Web Login System (Flask)**: Simple `/login` page, username & password stored in SQLite (`users.db`), secure validation backend.
* **Brute-Force Protection**: Detects repeated failed login attempts, counts attempts per IP, blocks attacker IP automatically (iptables), stores blocked IPs in `blocklist.txt`.
* **Database (SQLite)**: Lightweight, file-based user storage created by `create_db.py`.
* **Extensible**: Easy to add hashing, admin dashboard, unblock features, email alerts, rate-limiting, etc.

---

## 📁 Project Structure

```
BruteForceWeb/
│── app.py
│── brute_force.py
│── create_db.py
│── users.db
│── blocklist.txt
│── requirements.txt
│── templates/
│     └── login.html
```

---

## 🔧 Installation & Setup

1. **Clone the project**

```bash
git clone https://github.com/yourusername/BruteForceWeb.git
cd BruteForceWeb
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create the database**

```bash
python3 create_db.py
```

This creates `users.db` with the default user:

```
username: admin
password: 1234
```

---

## ▶️ Run the Web Application

```bash
python3 app.py
```

Open in browser: `http://localhost:5000`

---

## 🔐 Brute-Force Blocking Logic (How it works)

1. Every failed login call increments a counter for the request IP.
2. When the counter reaches the configured `THRESHOLD` (default: 5), the system will:

   * Block the IP at the **application level** (return HTTP 403 for future requests).
   * Optionally add an **iptables** rule to drop packets from that IP:

```
iptables -A INPUT -s <ip> -j DROP
```

3. Blocked IPs are appended to `blocklist.txt`.

---

## 📄 Files Explained

* `app.py` — Flask app: login route, DB validation, calls into brute-force module.
* `brute_force.py` — Brute-force protection logic: counting, blocking (iptables), blocklist management.
* `create_db.py` — Creates `users.db` and inserts a default user.
* `templates/login.html` — Frontend login page.
* `users.db` — SQLite file (created by `create_db.py`).
* `blocklist.txt` — Text file storing blocked IPs.

---

## 🧪 Testing Brute-Force Protection

1. Start the server:

```bash
python3 app.py
```

2. Open `http://localhost:5000` and enter invalid credentials repeatedly (>= threshold).
3. Confirm IP is in `blocklist.txt`:

```bash
cat blocklist.txt
```

4. If system-level blocking is enabled, check iptables:

```bash
sudo iptables -L
```

5. Attempt to access the site from the blocked IP — you should get a 403 or connection dropped.

---

## 🛠 Recommended Next Features

* Password hashing (bcrypt)
* Admin dashboard to view/unblock IPs
* Unblock timer (automatic unban after X minutes)
* Rate limiting per-IP and per-account
* Captcha (Google reCAPTCHA)
* Email alerts on block events
* Use `systemd` service to run the app in background

---

## ⚠️ Legal Warning

This tool is for **learning, defense, and authorized environments only**. Do **NOT** use it on systems or networks you do not own or have explicit permission to test.

---

## 🤝 Contributing

Pull requests and issues are welcome. If you add features, include tests and update the README accordingly.


