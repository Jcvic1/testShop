import os
from dotenv import load_dotenv

load_dotenv()

# POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
# POSTGRES_USER = os.environ.get("POSTGRES_USER")
# POSTGRES_DB = os.environ.get("POSTGRES_DB")
# POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

SECRET_KEY = os.environ.get("SECRET_KEY")
STRIPE_PUBLIC_KEY_USD = os.environ.get("STRIPE_PUBLIC_KEY_USD")
STRIPE_SECRET_KEY_USD = os.environ.get("STRIPE_SECRET_KEY_USD")

STRIPE_PUBLIC_KEY_POUND = os.environ.get("STRIPE_PUBLIC_KEY_POUND")
STRIPE_SECRET_KEY_POUND = os.environ.get("STRIPE_SECRET_KEY_POUND")

# POSTGRES_URL = os.environ.get("POSTGRES_URL")

# SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
# SMTP_USER = os.environ.get("SMTP_USER")

# REDIS_PORT = os.environ.get("REDIS_PORT")
# REDIS_HOST = os.environ.get("REDIS_HOST")
# REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
