import secrets
import string
from datetime import datetime, timedelta
from config import REFERRALS_CODE_VALIDITY, REFERRALS_CODE_LENGTH


def generate_random_code(length=REFERRALS_CODE_LENGTH):
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for _ in range(length))
    return code


def calculate_expiration_date():
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=REFERRALS_CODE_VALIDITY)
    return expiration_date
