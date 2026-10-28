from pathlib import Path
from dotenv import dotenv_values

BACKEND_ENV = Path("/usr/share/nginx/techstore/backend/.env")
ENV = dotenv_values(BACKEND_ENV)

SHARED_DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": ENV.get("DB_NAME"),
    "USER": ENV.get("DB_USER"),
    "PASSWORD": ENV.get("DB_PASSWORD"),
    "HOST": ENV.get("DB_HOST", "127.0.0.1"),
    "PORT": ENV.get("DB_PORT", "5432"),
    "CONN_MAX_AGE": 60,
    "OPTIONS": {},
}
