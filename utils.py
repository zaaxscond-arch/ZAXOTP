# utils.py - Helper functions

import os
import time
import random
import platform
import hashlib
import uuid
from datetime import datetime
from colorama import Fore, Style

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def get_date():
    now = datetime.now()
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{days[now.weekday()]}, {now.day} {months[now.month - 1]} {now.year}"

def get_device_id():
    """Generate unique device ID based on hardware"""
    try:
        identifiers = [
            platform.node(),
            platform.machine(),
            platform.processor(),
            str(uuid.getnode()),
        ]
        combined = "".join(identifiers)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    except:
        return hashlib.sha256(str(random.randint(1, 999999)).encode()).hexdigest()[:16]

def get_device_name():
    """Get device hostname"""
    try:
        return platform.node()
    except:
        return "Unknown Device"

def format_phone(phone):
    phone = ''.join(filter(str.isdigit, phone))
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    if not phone.startswith('62'):
        phone = '62' + phone
    return phone

def print_status(status, message):
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
    }
    icons = {
        "info": "[*]",
        "success": "[+]",
        "warning": "[!]",
        "error": "[-]",
    }
    color = colors.get(status, Fore.WHITE)
    icon = icons.get(status, "[*]")
    print(f"{color}{icon} {message}{Style.RESET_ALL}")
