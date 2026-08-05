# database.py - Sistem database dengan kode akses

import os
import json
from datetime import datetime
from utils import get_device_id

DB_FILE = "data/users.db"

# ========================================
# KODE AKSES LEVEL
# ========================================
ACCESS_CODES = {
    "XAZMODESAD": "owner",
    "BLINGBLING": "admin",
    "FCLOSE": "premium",
}

def init_db():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def load_db():
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(device_id=None):
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    return db.get(device_id)

def create_user(device_id=None, level="trial"):
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    
    if device_id not in db:
        db[device_id] = {
            "device_id": device_id,
            "level": level,
            "quota": -1 if level != "trial" else 50,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat(),
            "access_code": None,
        }
        save_db(db)
    return db[device_id]

def activate_with_code(device_id, code):
    """Aktivasi akses dengan kode"""
    if device_id is None:
        device_id = get_device_id()
    
    code = code.strip().upper()
    if code not in ACCESS_CODES:
        return False, "Kode tidak valid!"
    
    level = ACCESS_CODES[code]
    db = load_db()
    
    if device_id not in db:
        db[device_id] = {
            "device_id": device_id,
            "level": level,
            "quota": -1,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat(),
            "access_code": code,
        }
    else:
        db[device_id]["level"] = level
        db[device_id]["quota"] = -1
        db[device_id]["access_code"] = code
        db[device_id]["last_used"] = datetime.now().isoformat()
    
    save_db(db)
    return True, f"Akses {level.upper()} berhasil diaktifkan!"

def check_license(device_id=None):
    if device_id is None:
        device_id = get_device_id()
    user = get_user(device_id)
    
    if user is None:
        user = create_user(device_id, "trial")
    
    level = user.get("level", "trial")
    quota = user.get("quota", 50)
    
    if level in ["owner", "admin", "premium"]:
        return level, -1, device_id
    else:
        if quota <= 0:
            return "trial_expired", 0, device_id
        return "trial", quota, device_id

def use_quota(device_id=None):
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    
    if device_id not in db:
        return False
    
    user = db[device_id]
    level = user.get("level", "trial")
    
    # Owner, Admin, Premium = unlimited
    if level in ["owner", "admin", "premium"]:
        user["last_used"] = datetime.now().isoformat()
        save_db(db)
        return True
    
    if user.get("quota", 0) > 0:
        user["quota"] = user.get("quota", 0) - 1
        user["last_used"] = datetime.now().isoformat()
        save_db(db)
        return True
    
    return False

def get_user_stats():
    db = load_db()
    owner = sum(1 for u in db.values() if u.get("level") == "owner")
    admin = sum(1 for u in db.values() if u.get("level") == "admin")
    premium = sum(1 for u in db.values() if u.get("level") == "premium")
    trial = sum(1 for u in db.values() if u.get("level") == "trial" or u.get("level") is None)
    return {"owner": owner, "admin": admin, "premium": premium, "trial": trial}

def get_user_level(device_id=None):
    if device_id is None:
        device_id = get_device_id()
    user = get_user(device_id)
    if user:
        return user.get("level", "trial")
    return "trial"
