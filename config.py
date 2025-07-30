import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")  # Получить у @BotFather
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789")) if os.getenv("ADMIN_ID", "123456789").isdigit() else 123456789  # Ваш Telegram ID

# Telegram API для мониторинга каналов
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "YOUR_API_ID")  # Получить на https://my.telegram.org
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "YOUR_API_HASH")  # Получить на https://my.telegram.org

# Twitter API Keys
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", "YOUR_TWITTER_API_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", "YOUR_TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "YOUR_TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "YOUR_TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "YOUR_TWITTER_BEARER_TOKEN")

# PGP Encryption
PGP_RECIPIENT_EMAIL = os.getenv("PGP_RECIPIENT_EMAIL", "your-email@example.com")
GPG_HOME_DIR = os.getenv("GPG_HOME_DIR", "~/.gnupg")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./airdrop_hunter.db")

# Selenium Configuration
SELENIUM_WEBDRIVER_PATH = os.getenv("SELENIUM_WEBDRIVER_PATH", "/usr/local/bin/chromedriver")
SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "./screenshots")

# Airdrop filter options
VALID_BLOCKCHAINS = ["ton", "ethereum", "solana", "bsc", "polygon", "arbitrum", "aptos"]

# API Rate Limits
TWITTER_RATE_LIMIT = 300  # requests per 15 minutes

# Instructions for obtaining API keys:
# 1. Telegram Bot Token: Write to @BotFather on Telegram
# 2. Telegram API ID/Hash: Go to https://my.telegram.org
# 3. Twitter API: Apply at https://developer.twitter.com 