import os
import logging


API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL),
)

# Configure the enabled apps
APPS = ['basic', 'poll']
