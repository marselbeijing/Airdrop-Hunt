# 🔑 Настройка API для Airdrop Hunter

## 📋 Содержание
1. [CoinMarketCap API](#coinmarketcap-api)
2. [Twitter API](#twitter-api)
3. [Telegram Bot API](#telegram-bot-api)
4. [Настройка переменных окружения](#настройка-переменных-окружения)
5. [Тестирование API](#тестирование-api)

---

## 1. CoinMarketCap API

### 🎯 Что это дает:
- Реальные данные об аирдропах
- Актуальная информация о проектах
- Автоматическое обновление базы данных

### 📝 Пошаговая настройка:

1. **Регистрация:**
   - Перейдите на https://coinmarketcap.com/api/
   - Нажмите "Get Started"
   - Создайте аккаунт

2. **Выбор плана:**
   - Выберите "Basic" (бесплатный)
   - 10,000 запросов в месяц
   - Доступ к основным данным

3. **Получение ключа:**
   - В личном кабинете найдите "API Keys"
   - Скопируйте ваш API ключ

4. **Установка:**
   ```bash
   export COINMARKETCAP_API_KEY="ваш_ключ_здесь"
   ```

---

## 2. Twitter API

### 🎯 Что это дает:
- Автоматическое подписание на аккаунты проектов
- Ретвиты и лайки постов
- Взаимодействие с сообществом

### 📝 Пошаговая настройка:

1. **Создание приложения:**
   - Перейдите на https://developer.twitter.com/
   - Нажмите "Apply for a developer account"
   - Заполните анкету (может занять 1-2 дня)

2. **Создание проекта:**
   - В Developer Portal создайте новый проект
   - Добавьте приложение в проект

3. **Получение ключей:**
   - Consumer Key (API Key)
   - Consumer Secret (API Secret)
   - Access Token
   - Access Token Secret

4. **Настройка разрешений:**
   - В настройках приложения включите:
     - Read and Write permissions
     - Direct Message permissions

5. **Установка:**
   ```bash
   export TWITTER_CONSUMER_KEY="ваш_consumer_key"
   export TWITTER_CONSUMER_SECRET="ваш_consumer_secret"
   export TWITTER_ACCESS_TOKEN="ваш_access_token"
   export TWITTER_ACCESS_TOKEN_SECRET="ваш_access_token_secret"
   ```

---

## 3. Telegram Bot API

### 🎯 Что это дает:
- Автоматический бот для пользователей
- Уведомления о новых аирдропах
- Интерактивные команды

### 📝 Пошаговая настройка:

1. **Создание бота:**
   - Найдите @BotFather в Telegram
   - Отправьте команду `/newbot`
   - Следуйте инструкциям

2. **Получение токена:**
   - BotFather выдаст токен вида:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

3. **Установка:**
   ```bash
   export BOT_TOKEN="ваш_токен_бота"
   ```

4. **Настройка команд:**
   - Отправьте @BotFather команду `/setcommands`
   - Добавьте команды бота

---

## 4. Настройка переменных окружения

### 📁 Создание .env файла:

```bash
# Создайте файл .env в корне проекта
touch .env
```

### 📝 Содержимое .env файла:

```env
# Telegram Bot
BOT_TOKEN=ваш_токен_бота

# Database
DATABASE_URL=sqlite:///./airdrop_hunter.db

# CoinMarketCap API
COINMARKETCAP_API_KEY=ваш_coinmarketcap_ключ

# Twitter API
TWITTER_CONSUMER_KEY=ваш_twitter_consumer_key
TWITTER_CONSUMER_SECRET=ваш_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=ваш_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=ваш_twitter_access_token_secret

# Admin
ADMIN_ID=ваш_telegram_id

# Selenium
SELENIUM_WEBDRIVER_PATH=/usr/local/bin/chromedriver
SCREENSHOTS_DIR=./screenshots

# PGP (опционально)
PGP_RECIPIENT_EMAIL=ваш_email@example.com
```

### 🔧 Установка переменных:

```bash
# Загрузите переменные из .env файла
source .env

# Или установите вручную
export BOT_TOKEN="ваш_токен"
export COINMARKETCAP_API_KEY="ваш_ключ"
# ... и так далее
```

---

## 5. Тестирование API

### 🧪 Проверка CoinMarketCap:

```python
import requests

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrops"
headers = {
    'X-CMC_PRO_API_KEY': 'ваш_ключ',
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Data: {response.json()}")
```

### 🧪 Проверка Twitter:

```python
import tweepy

auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")
api = tweepy.API(auth)

user = api.verify_credentials()
print(f"Connected as: @{user.screen_name}")
```

### 🧪 Проверка Telegram:

```python
import asyncio
from aiogram import Bot

async def test_bot():
    bot = Bot(token="ваш_токен")
    me = await bot.get_me()
    print(f"Bot: @{me.username}")
    await bot.session.close()

asyncio.run(test_bot())
```

---

## ⚠️ Важные замечания

### 🔒 Безопасность:
- Никогда не коммитьте API ключи в git
- Используйте .env файл (добавьте в .gitignore)
- Регулярно обновляйте ключи

### 📊 Лимиты:
- **CoinMarketCap**: 10,000 запросов/месяц (Basic)
- **Twitter**: 300 запросов/15 минут
- **Telegram**: 30 сообщений/секунду

### 🛠️ Устранение проблем:

1. **"Invalid API Key"** - Проверьте правильность ключа
2. **"Rate limit exceeded"** - Подождите или обновите план
3. **"Unauthorized"** - Проверьте права доступа

---

## 🚀 Запуск с API

После настройки всех API:

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Запустите приложение
python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

Теперь ваше приложение будет использовать реальные API! 🎉 