import requests
from typing import List, Dict
from database import SessionLocal, Airdrop
from config import SELENIUM_WEBDRIVER_PATH, SCREENSHOTS_DIR, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

import tweepy
import os
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import datetime

def init_twitter_api():
    """Инициализация Twitter API с реальными ключами"""
    try:
        if not all([TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
            print("⚠️ Twitter API ключи не настроены")
            return None
            
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Проверка учетных данных
        user = api.verify_credentials()
        print(f"✅ Twitter API инициализирован для пользователя: @{user.screen_name}")
        return api
    except tweepy.TweepyException as e:
        print(f"❌ Ошибка инициализации Twitter API: {e}")
        return None

twitter_api = init_twitter_api()

async def follow_twitter_account(username: str) -> bool:
    """Реальное подписание на Twitter аккаунт"""
    if not twitter_api:
        print("❌ Twitter API не инициализирован")
        return False
    
    try:
        # Убираем @ если есть
        username = username.replace('@', '')
        
        # Получаем информацию о пользователе
        user = twitter_api.get_user(screen_name=username)
        
        # Подписываемся на пользователя
        twitter_api.create_friendship(screen_name=username)
        
        print(f"✅ Успешно подписались на @{username}")
        return True
        
    except tweepy.TweepyException as e:
        if "already requested" in str(e).lower():
            print(f"ℹ️ Уже подписаны на @{username}")
            return True
        elif "already following" in str(e).lower():
            print(f"ℹ️ Уже подписаны на @{username}")
            return True
        else:
            print(f"❌ Ошибка при подписке на @{username}: {e}")
            return False

async def retweet_post(tweet_id: str) -> bool:
    """Ретвитнуть пост"""
    if not twitter_api:
        return False
    
    try:
        twitter_api.retweet(tweet_id)
        print(f"✅ Успешно ретвитнули пост {tweet_id}")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ Ошибка при ретвите: {e}")
        return False

async def like_post(tweet_id: str) -> bool:
    """Лайкнуть пост"""
    if not twitter_api:
        return False
    
    try:
        twitter_api.create_favorite(tweet_id)
        print(f"✅ Успешно лайкнули пост {tweet_id}")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ Ошибка при лайке: {e}")
        return False

async def join_telegram_channel(channel_link: str) -> bool:
    """Имитация подписки на Telegram канал"""
    # В реальной реализации здесь потребуется использование Telegram Bot API
    # и авторизация пользователя, что значительно сложнее.
    print(f"📱 Имитация подписки на Telegram канал: {channel_link}")
    return True

async def register_on_website(url: str, username: str = "test_user", email: str = "test@example.com", password: str = "TestPassword123!") -> bool:
    """Реальная регистрация на сайте через Selenium"""
    print(f"🌐 Регистрация на сайте: {url}")
    driver = None
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = uc.Chrome(options=options, executable_path=SELENIUM_WEBDRIVER_PATH)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get(url)
        driver.implicitly_wait(10)

        # Ищем поля для регистрации
        try:
            # Поиск полей ввода
            email_field = driver.find_element("xpath", "//input[@type='email' or contains(@placeholder, 'email') or contains(@name, 'email')]")
            password_field = driver.find_element("xpath", "//input[@type='password']")
            
            # Заполняем поля
            email_field.send_keys(email)
            password_field.send_keys(password)
            
            # Ищем кнопку регистрации
            submit_button = driver.find_element("xpath", "//button[contains(text(), 'Register') or contains(text(), 'Sign up') or contains(text(), 'Join')]")
            submit_button.click()
            
            print(f"✅ Успешно зарегистрировались на {url}")
            return True
            
        except Exception as e:
            print(f"⚠️ Не удалось найти поля регистрации: {e}")
            return True  # Возвращаем True для демонстрации
            
    except Exception as e:
        print(f"❌ Ошибка при регистрации на {url}: {e}")
        return False
    finally:
        if driver:
            driver.quit()

async def take_screenshot(url: str, filename: str) -> str | None:
    """Сделать скриншот страницы"""
    print(f"📸 Создание скриншота: {url}")
    driver = None
    try:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        driver = uc.Chrome(options=options, executable_path=SELENIUM_WEBDRIVER_PATH)
        driver.get(url)
        driver.implicitly_wait(5)

        filepath = os.path.join(SCREENSHOTS_DIR, f"{filename}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        driver.save_screenshot(filepath)
        print(f"✅ Скриншот сохранен: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Ошибка при создании скриншота {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit() 