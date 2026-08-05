# database.py - Sistem database plain JSON (no encryption)

import os
import json
from datetime import datetime, timedelta
from utils import get_device_id

DB_FILE = "data/users.db"

def init_db():
    """Inisialisasi database"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def load_db():
    """Load database"""
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    """Save database"""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(device_id=None):
    """Get user by device_id"""
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    return db.get(device_id)

def create_user(device_id=None, is_premium=False):
    """Create new user"""
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    
    if device_id not in db:
        db[device_id] = {
            "device_id": device_id,
            "is_premium": is_premium,
            "quota": 50 if not is_premium else -1,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat(),
        }
        save_db(db)
    return db[device_id]

def check_license(device_id=None):
    """Check user license status"""
    if device_id is None:
        device_id = get_device_id()
    user = get_user(device_id)
    
    if user is None:
        user = create_user(device_id)
    
    if user.get("is_premium", False):
        return "premium", -1, device_id
    else:
        quota = user.get("quota", 50)
        if quota <= 0:
            return "trial_expired", 0, device_id
        return "trial", quota, device_id

def use_quota(device_id=None):
    """Reduce quota by 1"""
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    
    if device_id not in db:
        return False
    
    user = db[device_id]
    if user.get("is_premium", False):
        user["last_used"] = datetime.now().isoformat()
        save_db(db)
        return True
    
    if user.get("quota", 0) > 0:
        user["quota"] = user.get("quota", 0) - 1
        user["last_used"] = datetime.now().isoformat()
        save_db(db)
        return True
    
    return False

def activate_premium(device_id=None):
    """Activate premium for user"""
    if device_id is None:
        device_id = get_device_id()
    db = load_db()
    
    if device_id not in db:
        db[device_id] = {
            "device_id": device_id,
            "is_premium": True,
            "quota": -1,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat(),
        }
    else:
        db[device_id]["is_premium"] = True
        db[device_id]["quota"] = -1
        db[device_id]["last_used"] = datetime.now().isoformat()
    
    save_db(db)
    return True

def get_user_stats():
    """Get total user stats"""
    db = load_db()
    premium = sum(1 for u in db.values() if u.get("is_premium", False))
    trial = sum(1 for u in db.values() if not u.get("is_premium", False))
    return premium, trial
