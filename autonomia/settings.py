import logging
import os

# application configuration
DEBUG = os.environ.get("DEBUG", "False") == "True"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL),
)
WEBHOOK_DOMAIN = os.environ.get("WEBHOOK_DOMAIN", "localhost:5000")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH", "hook")

# Third party configuration
API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")
FIXER_IO_API_TOKEN = os.environ.get("FIXER_IO_API_TOKEN", "")
MEETUP_API_KEY = os.environ.get("MEETUP_API_KEY", "")

# Configure the enabled apps
APPS = [
    "basic",
    "poll",
    "help",
    "weather",
    "meetup",
    "currency",
    "dublin_bus",
    "dublin_bike",
]
