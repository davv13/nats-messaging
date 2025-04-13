import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL Configuration
DB_NAME = os.getenv("DB_NAME", "nats_messages_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "defaultpassword")  # Default fallback
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# NATS Configuration
NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")