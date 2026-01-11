import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def authenticate(email, password):
    users = load_users()
    if email in users and users[email]["password"] == password:
        return True
    return False

