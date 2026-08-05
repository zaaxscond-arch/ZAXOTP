# zaxotp/core.py - Core functions

from spammer import OTPSpammer
from database import check_license, use_quota, activate_premium, get_user_stats
from utils import get_device_id, format_phone
from config import VERSION

__all__ = [
    "OTPSpammer",
    "check_license",
    "use_quota",
    "activate_premium",
    "get_user_stats",
    "get_device_id",
    "format_phone",
    "VERSION",
]
