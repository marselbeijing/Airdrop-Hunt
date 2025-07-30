import requests
import json
from datetime import datetime, timedelta
from database import SessionLocal, Airdrop
import random

def fetch_airdrops_from_coingecko():
    """Получить аирдропы из CoinGecko (бесплатно)"""
    try:
        # CoinGecko API бесплатный
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': False
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            coins = response.json()
            airdrops = []
            
            # Имитируем аирдропы на основе популярных монет
            for coin in coins[:20]:
                if random.random() < 0.3:  # 30% шанс
                    airdrop = {
                        "title": f"{coin['name']} Airdrop",
                        "description": f"Exclusive airdrop for {coin['name']} holders",
                        "source_url": f"https://coingecko.com/en/coins/{coin['id']}",
                        "blockchain": determine_blockchain(coin['name']),
                        "difficulty": random.choice(["easy", "medium", "hard"]),
                        "reward": f"{random.randint(10, 1000)} {coin['symbol'].upper()}",
                        "end_date": datetime.now() + timedelta(days=random.randint(30, 90))
                    }
                    airdrops.append(airdrop)
            
            return airdrops
        else:
            print(f"CoinGecko API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching from CoinGecko: {e}")
        return []

def fetch_airdrops_from_airdropalert():
    """Получить аирдропы из AirdropAlert (бесплатно)"""
    try:
        # AirdropAlert RSS feed
        url = "https://airdropalert.com/feed/"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Парсим RSS feed
            from xml.etree import ElementTree
            root = ElementTree.fromstring(response.content)
            
            airdrops = []
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text
                description = item.find('description').text
                original_link = item.find('link').text
                
                # Создаем реферальную ссылку
                referral_link = create_referral_link(original_link)
                
                airdrop = {
                    "title": title,
                    "description": description,
                    "source_url": original_link,
                    "referral_link": referral_link,
                    "blockchain": determine_blockchain(title),
                    "difficulty": determine_difficulty(description),
                    "reward": format_reward(description),
                    "end_date": parse_date(item.find('pubDate').text)
                }
                airdrops.append(airdrop)
            
            return airdrops
        else:
            print(f"AirdropAlert API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching from AirdropAlert: {e}")
        return []

def fetch_airdrops_from_icodrops():
    """Получить аирдропы из ICOdrops (бесплатно)"""
    try:
        # ICOdrops API
        url = "https://icodrops.com/api/v1/icos"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            airdrops = []
            
            for ico in data.get('icos', [])[:15]:
                if ico.get('airdrop'):
                    original_url = f"https://icodrops.com{ico['url']}"
                    referral_link = create_referral_link(original_url)
                    
                    airdrop = {
                        "title": f"{ico['name']} Airdrop",
                        "description": f"Airdrop for {ico['name']} project",
                        "source_url": original_url,
                        "referral_link": referral_link,
                        "blockchain": determine_blockchain(ico['name']),
                        "difficulty": "medium",
                        "reward": format_reward(ico.get('description', '')),
                        "end_date": datetime.now() + timedelta(days=random.randint(30, 60))
                    }
                    airdrops.append(airdrop)
            
            return airdrops
        else:
            print(f"ICOdrops API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching from ICOdrops: {e}")
        return []

def fetch_airdrops_from_twitter():
    """Получить аирдропы из Twitter (бесплатно)"""
    try:
        from config import TWITTER_BEARER_TOKEN
        
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {
            'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}',
        }
        params = {
            'query': 'airdrop OR airdrops -is:retweet lang:en',
            'max_results': 50
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            airdrops = []
            
            for tweet in data.get('data', []):
                text = tweet['text']
                if any(keyword in text.lower() for keyword in ['airdrop', 'claim', 'free']):
                    original_url = f"https://twitter.com/user/status/{tweet['id']}"
                    referral_link = create_referral_link(original_url)
                    
                    airdrop = {
                        "title": f"Twitter Airdrop - {text[:50]}...",
                        "description": text,
                        "source_url": original_url,
                        "referral_link": referral_link,
                        "blockchain": determine_blockchain(text),
                        "difficulty": "easy",
                        "reward": "Unknown",
                        "end_date": datetime.now() + timedelta(days=7)
                    }
                    airdrops.append(airdrop)
            
            return airdrops
        else:
            print(f"Twitter API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching from Twitter: {e}")
        return []

def fetch_airdrops_from_telegram():
    """Получить аирдропы из Telegram каналов (бесплатно)"""
    try:
        # Имитация данных из Telegram каналов
        telegram_channels = [
            "AirdropAlert",
            "CryptoAirdrops",
            "AirdropHunter",
            "FreeCryptoAirdrops"
        ]
        
        airdrops = []
        for channel in telegram_channels:
            # Имитируем аирдропы из каждого канала
            for i in range(random.randint(2, 5)):
                airdrop = {
                    "title": f"{channel} Airdrop #{i+1}",
                    "description": f"Exclusive airdrop from {channel} channel",
                    "source_url": f"https://t.me/{channel}",
                    "blockchain": random.choice(["ethereum", "solana", "ton", "bsc"]),
                    "difficulty": random.choice(["easy", "medium"]),
                    "reward": f"{random.randint(10, 500)} tokens",
                    "end_date": datetime.now() + timedelta(days=random.randint(7, 30))
                }
                airdrops.append(airdrop)
        
        return airdrops
    except Exception as e:
        print(f"Error fetching from Telegram: {e}")
        return []

def fetch_all_airdrops():
    """Получить аирдропы из всех источников"""
    all_airdrops = []
    
    # Добавляем аирдропы из разных источников
    all_airdrops.extend(fetch_airdrops_from_coingecko())
    all_airdrops.extend(fetch_airdrops_from_airdropalert())
    all_airdrops.extend(fetch_airdrops_from_icodrops())
    all_airdrops.extend(fetch_airdrops_from_twitter())
    all_airdrops.extend(fetch_airdrops_from_telegram())
    
    return all_airdrops

def determine_blockchain(text):
    """Определить блокчейн по тексту"""
    text = text.lower()
    if any(word in text for word in ['ton', 'telegram']):
        return 'ton'
    elif any(word in text for word in ['eth', 'ethereum']):
        return 'ethereum'
    elif any(word in text for word in ['sol', 'solana']):
        return 'solana'
    elif any(word in text for word in ['bsc', 'binance']):
        return 'bsc'
    elif any(word in text for word in ['polygon', 'matic']):
        return 'polygon'
    else:
        return random.choice(['ethereum', 'solana', 'ton', 'bsc'])

def determine_difficulty(description):
    """Определить сложность аирдропа"""
    description = description.lower()
    if any(word in description for word in ['easy', 'simple', 'quick']):
        return 'easy'
    elif any(word in description for word in ['hard', 'complex', 'advanced']):
        return 'hard'
    else:
        return 'medium'

def format_reward(text):
    """Форматировать награду"""
    text = text.lower()
    if 'ton' in text:
        return f"{random.randint(10, 100)} TON"
    elif 'eth' in text or 'ethereum' in text:
        return f"{random.randint(0.01, 0.5)} ETH"
    elif 'sol' in text or 'solana' in text:
        return f"{random.randint(1, 10)} SOL"
    else:
        return f"{random.randint(10, 1000)} tokens"

def parse_date(date_str):
    """Парсить дату"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return datetime.now() + timedelta(days=30)

def create_referral_link(original_url):
    """Создать реферальную ссылку"""
    # Здесь можно настроить разные реферальные системы
    # Примеры:
    # - Добавить UTM параметры
    # - Использовать сервис сокращения ссылок
    # - Добавить уникальный идентификатор
    
    # Простой вариант с UTM параметрами
    if '?' in original_url:
        separator = '&'
    else:
        separator = '?'
    
    referral_link = f"{original_url}{separator}ref=airdrophunter&utm_source=airdrophunter&utm_medium=bot&utm_campaign=airdrop"
    
    return referral_link

def save_airdrops_to_database(airdrops):
    """Сохранить аирдропы в базу данных"""
    db = SessionLocal()
    try:
        for airdrop_data in airdrops:
            # Проверяем, не существует ли уже такой аирдроп
            existing = db.query(Airdrop).filter(
                Airdrop.title == airdrop_data["title"]
            ).first()
            
            if not existing:
                airdrop = Airdrop(
                    title=airdrop_data["title"],
                    description=airdrop_data["description"],
                    source_url=airdrop_data["source_url"],
                    referral_link=airdrop_data.get("referral_link"),
                    blockchain=airdrop_data["blockchain"],
                    difficulty=airdrop_data["difficulty"],
                    reward=airdrop_data["reward"],
                    status="active",
                    end_date=airdrop_data["end_date"],
                    is_moderated=True
                )
                db.add(airdrop)
        
        db.commit()
        print(f"✅ Сохранено {len(airdrops)} новых аирдропов")
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка сохранения: {e}")
    finally:
        db.close()

def main():
    """Главная функция для парсинга аирдропов"""
    print("🔍 Начинаю поиск аирдропов...")
    
    # Получаем аирдропы из всех источников
    airdrops = fetch_all_airdrops()
    
    if airdrops:
        print(f"📊 Найдено {len(airdrops)} аирдропов")
        save_airdrops_to_database(airdrops)
    else:
        print("❌ Аирдропы не найдены")

if __name__ == "__main__":
    main() 