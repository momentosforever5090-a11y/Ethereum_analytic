import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key-change-in-production')
    # Si usas PostgreSQL más adelante, añade:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
