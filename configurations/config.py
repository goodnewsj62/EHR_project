import os
import secrets
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(find_dotenv())


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SECRET_KEY = secrets.token_hex(32)
    FLASK_ADMIN_SWATCH = "sandstone"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 100 * 1024
    SQLALCHEMY_BINDS = {"sqldb": "sqlite:///sitedbl.db"}
    ALLOWED_EXTENSIONS = set(["jpg", "png", "webp"])
    PER_PAGE = 20


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
