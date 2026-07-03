# config.py
# Yeh file .env se saari secret values (DB password, JWT secret, etc.) load karti hai

import os
from dotenv import load_dotenv

# .env file ko load karo
load_dotenv()

# Database settings
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

# OpenAI settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")