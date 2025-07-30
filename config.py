import os

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8399460650:AAGa6PBJa1hTw1dPV-kyMR5GeQYOGbdraiE")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./airdrop_hunter.db")

# API Keys Configuration
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY", "189714b7-cc83-4921-8686-cf1596735299")

# Twitter API Configuration
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", "4R5C7lVc7j99XmxjNsLlRJh6A")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", "92DiXGDQAZ2gZg02UuqsIgOOwzSF6TmKnqGaCRgxvbHGVZED9q")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "1767843477050609664-GOYE0Tg6v079pMNipDpRRajwr7P7sr")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "Of3HrGV45KySZfGekqD3zsCc4cUpWgw9DneSOAOvrIDJG")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "AAAAAAAAAAAAAAAAAAAAACE83QEAAAAAVHUb4%2BwUCcETbOjaa2YBiFoVPys%3DhQTyMAB0SSDhtdyWtCyBM40h6lDlLWIRoVUD4pwjfXmRpFfn1t")

# Selenium Configuration
SELENIUM_WEBDRIVER_PATH = os.getenv("SELENIUM_WEBDRIVER_PATH", "/usr/local/bin/chromedriver")
SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "./screenshots")

# Admin settings
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# Airdrop filter options
VALID_BLOCKCHAINS = ["ton", "ethereum", "solana", "bsc", "polygon", "arbitrum", "aptos"]

# PGP Configuration
PGP_RECIPIENT_EMAIL = os.getenv("PGP_RECIPIENT_EMAIL", "your_email@example.com")
GPG_HOME_DIR = os.getenv("GPG_HOME_DIR", os.path.expanduser("~/.gnupg"))

# API Rate Limits
COINMARKETCAP_RATE_LIMIT = 10000  # requests per month
TWITTER_RATE_LIMIT = 300  # requests per 15 minutes

# Instructions for API Keys:
"""
🔑 КАК ПОЛУЧИТЬ API КЛЮЧИ:

1. COINMARKETCAP API:
   - Зайдите на https://coinmarketcap.com/api/
   - Зарегистрируйтесь и выберите план (Basic бесплатный)
   - Скопируйте API ключ
   - Установите: export COINMARKETCAP_API_KEY="ваш_ключ"

2. TWITTER API:
   - Зайдите на https://developer.twitter.com/
   - Создайте приложение
   - Получите Consumer Key, Consumer Secret, Access Token, Access Token Secret
   - Установите переменные окружения

3. TELEGRAM BOT:
   - Напишите @BotFather в Telegram
   - Создайте бота командой /newbot
   - Получите токен и установите: export BOT_TOKEN="ваш_токен"
""" 