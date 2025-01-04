import os
import secrets
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(find_dotenv())


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ADMIN_SWATCH = "sandstone"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 100 * 1024
    ALLOWED_EXTENSIONS = set(["jpg", "png", "webp"])
    PER_PAGE = 20
    # Configure Flask-Mail settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587  # Replace with your email server's port
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("EHR", "noreply@gmail.com")


class DevelopmentConfig(Config):
    DEBUG = True
    ENV_ = "dev"
    MEDIA_PATH = BASE_DIR / os.getenv("MEDIA_PATH")
    # SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    ENV_ = "production"
    SECRET_KEY = os.getenv("SECRET_KEY")
    ADMINS = ["osonwajohn@gmail.com"]
    MEDIA_PATH = Path(os.getenv("MEDIA_PATH"))
