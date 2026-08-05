# license.py - Wrapper sederhana (tanpa enkripsi)

from database import (
    get_user,
    create_user,
    check_license,
    use_quota,
    activate_premium,
    get_user_stats,
)
from config import (
    TRIAL_QUOTA,
    LICENSE_PRICE,
    WHATSAPP_ADMIN,
    TELEGRAM_USERNAME,
    VERSION,
    TOOLS_NAME,
)
from utils import get_device_id, clear_screen, print_status
from banner import BANNER

def log_header():
    """Print header dengan banner"""
    clear_screen()
    print(BANNER)
