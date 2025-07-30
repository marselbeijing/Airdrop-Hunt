#!/usr/bin/env python3
"""
🧪 Тестирование API для Airdrop Hunter
"""

import os
import asyncio
import requests
import tweepy
from aiogram import Bot
from config import (
    COINMARKETCAP_API_KEY, 
    TWITTER_CONSUMER_KEY, 
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    BOT_TOKEN
)

def test_coinmarketcap_api():
    """Тест CoinMarketCap API"""
    print("🔍 Тестирование CoinMarketCap API...")
    
    if COINMARKETCAP_API_KEY == "YOUR_COINMARKETCAP_API_KEY":
        print("❌ API ключ не настроен")
        return False
    
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrops"
        headers = {
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            airdrops_count = len(data.get('data', []))
            print(f"✅ CoinMarketCap API работает! Найдено аирдропов: {airdrops_count}")
            return True
        else:
            print(f"❌ Ошибка API: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании CoinMarketCap API: {e}")
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

async def test_telegram_bot():
    """Тест Telegram Bot API"""
    print("📱 Тестирование Telegram Bot API...")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ Токен бота не настроен")
        return False
    
    try:
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Telegram Bot API работает! Бот: @{me.username}")
        await bot.session.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании Telegram Bot API: {e}")
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

async def main():
    """Основная функция тестирования"""
    print("🧪 Запуск тестирования API...\n")
    
    results = {
        "CoinMarketCap": test_coinmarketcap_api(),
        "Twitter": test_twitter_api(),
        "Telegram": await test_telegram_bot(),
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
    asyncio.run(main()) 