from dotenv import load_dotenv
import os

load_dotenv()

# DB Data
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# DB Data test
DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")


# Referrals Code
REFERRALS_CODE_VALIDITY = int(os.environ.get("REFERRALS_CODE_VALIDITY"))
REFERRALS_CODE_LENGTH = int(os.environ.get("REFERRALS_CODE_LENGTH"))

# HunterEmail
EMAIL_API_KEY = os.environ.get("EMAILHUNTER_APIKEY")

# Secret
SECRET = os.environ.get("SECRET")

# Redis
BROKER_URL = os.environ.get("BROKER_URL")
RESULT_BACKEND = os.environ.get("RESULT_BACKEND")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
