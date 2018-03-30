import os
import logging


API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Configure the enabled apps
APPS = ['basic']
