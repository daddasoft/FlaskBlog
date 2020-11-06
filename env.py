# settings.py
from pathlib import Path  # Python 3.6+ only
from dotenv import load_dotenv
import os
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def env(key):
    return os.getenv(key)
