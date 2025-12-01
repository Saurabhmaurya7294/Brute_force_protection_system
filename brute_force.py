import subprocess
from datetime import datetime

THRESHOLD = 5

failed_attempts = {}
blocked_ips = set()


def block_ip(ip):
    if ip in blocked_ips:
        return

    # Block using iptables
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

    # Save blocked IP
    with open("blocklist.txt", "a") as f:
        f.write(f"{ip}\n")

    blocked_ips.add(ip)
    print(f"[BLOCKED] IP: {ip}")


def register_failed_attempt(ip):
    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
    print(f"Failed attempt from {ip}: {failed_attempts[ip]}")

    if failed_attempts[ip] >= THRESHOLD:
        block_ip(ip)
