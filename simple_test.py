#!/usr/bin/env python3
"""
🧪 Простой тест API для Airdrop Hunter
"""

import requests
import tweepy
from config import (
    TWITTER_CONSUMER_KEY, 
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    BOT_TOKEN
)

def test_telegram_bot():
    """Тест Telegram Bot API через HTTP"""
    print("📱 Тестирование Telegram Bot API...")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ Токен бота не настроен")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Telegram Bot API работает! Бот: @{bot_info['username']}")
                return True
            else:
                print(f"❌ Ошибка Telegram API: {data}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании Telegram Bot API: {e}")
        return False

def test_twitter_api():
    """Тест Twitter API"""
    print("🐦 Тестирование Twitter API...")
    
    if not all([TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("❌ Twitter API ключи не настроены")
        return False
    
    try:
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        user = api.verify_credentials()
        print(f"✅ Twitter API работает! Подключен как: @{user.screen_name}")
        return True
        
    except tweepy.TweepyException as e:
        print(f"❌ Ошибка Twitter API: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании Twitter API: {e}")
        return False

def test_database():
    """Тест базы данных"""
    print("🗄️ Тестирование базы данных...")
    
    try:
        from database import SessionLocal, init_db
        from sqlalchemy import text
        
        # Инициализируем базу данных
        init_db()
        
        # Тестируем подключение
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        print("✅ База данных работает!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании базы данных: {e}")
        return False

def test_selenium():
    """Тест Selenium"""
    print("🌐 Тестирование Selenium...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Selenium работает! Загружена страница: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании Selenium: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Запуск тестирования API...\n")
    
    results = {
        "Twitter": test_twitter_api(),
        "Telegram": test_telegram_bot(),
        "Database": test_database(),
        "Selenium": test_selenium()
    }
    
    print("\n📊 Результаты тестирования:")
    print("=" * 40)
    
    working_apis = 0
    for api_name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {api_name}")
        if status:
            working_apis += 1
    
    print("=" * 40)
    print(f"🎯 Работает API: {working_apis}/{len(results)}")
    
    if working_apis == len(results):
        print("🎉 Все API работают отлично!")
    elif working_apis > 0:
        print("⚠️ Некоторые API не настроены, но приложение будет работать")
    else:
        print("❌ Ни один API не работает. Проверьте настройки.")

if __name__ == "__main__":
    main() 