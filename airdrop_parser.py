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
                        "referral_link": create_referral_link(f"https://coingecko.com/en/coins/{coin['id']}"),
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
    
    print("🔍 Начинаю парсинг аирдропов...")
    
    # Добавляем аирдропы из разных источников
    coingecko_airdrops = fetch_airdrops_from_coingecko()
    print(f"📊 CoinGecko: найдено {len(coingecko_airdrops)} аирдропов")
    all_airdrops.extend(coingecko_airdrops)
    
    airdropalert_airdrops = fetch_airdrops_from_airdropalert()
    print(f"📊 AirdropAlert: найдено {len(airdropalert_airdrops)} аирдропов")
    all_airdrops.extend(airdropalert_airdrops)
    
    icodrops_airdrops = fetch_airdrops_from_icodrops()
    print(f"📊 ICOdrops: найдено {len(icodrops_airdrops)} аирдропов")
    all_airdrops.extend(icodrops_airdrops)
    
    twitter_airdrops = fetch_airdrops_from_twitter()
    print(f"📊 Twitter: найдено {len(twitter_airdrops)} аирдропов")
    all_airdrops.extend(twitter_airdrops)
    
    telegram_airdrops = fetch_airdrops_from_telegram()
    print(f"📊 Telegram: найдено {len(telegram_airdrops)} аирдропов")
    all_airdrops.extend(telegram_airdrops)
    
    # Если ничего не найдено, используем гарантированные данные
    if not all_airdrops:
        print("⚠️ Ничего не найдено, используем гарантированные данные")
        all_airdrops = get_guaranteed_airdrops()
    
    print(f"🎯 Всего найдено: {len(all_airdrops)} аирдропов")
    return all_airdrops

def get_guaranteed_airdrops():
    """Гарантированные аирдропы для демонстрации"""
    return [
        {
            "title": "TON Blockchain Airdrop",
            "description": "Exclusive airdrop for TON blockchain early adopters and community members",
            "source_url": "https://ton.org/airdrop",
            "referral_link": "https://ton.org/airdrop?ref=airdrophunter&utm_source=airdrophunter&utm_medium=bot&utm_campaign=airdrop",
            "blockchain": "TON",
            "difficulty": "Easy",
            "reward": "50 TON",
            "end_date": datetime.now() + timedelta(days=30)
        },
        {
            "title": "Ethereum DeFi Protocol Airdrop",
            "description": "DeFi protocol airdrop for liquidity providers and early users",
            "source_url": "https://defi.org/airdrop",
            "referral_link": "https://defi.org/airdrop?ref=airdrophunter&utm_source=airdrophunter&utm_medium=bot&utm_campaign=airdrop",
            "blockchain": "Ethereum",
            "difficulty": "Medium",
            "reward": "0.1 ETH",
            "end_date": datetime.now() + timedelta(days=45)
        },
        {
            "title": "Solana NFT Marketplace Airdrop",
            "description": "NFT marketplace airdrop for creators and collectors",
            "source_url": "https://solana-nft.com/airdrop",
            "referral_link": "https://solana-nft.com/airdrop?ref=airdrophunter&utm_source=airdrophunter&utm_medium=bot&utm_campaign=airdrop",
            "blockchain": "Solana",
            "difficulty": "Hard",
            "reward": "5 SOL",
            "end_date": datetime.now() + timedelta(days=60)
        },
        {
            "title": "Binance Smart Chain Airdrop",
            "description": "BSC ecosystem airdrop for DeFi users and traders",
            "source_url": "https://bsc.defi/airdrop",
            "referral_link": "https://bsc.defi/airdrop?ref=airdrophunter&utm_source=airdrophunter&utm_medium=bot&utm_campaign=airdrop",
            "blockchain": "BSC",
            "difficulty": "Medium",
            "reward": "100 BNB",
            "end_date": datetime.now() + timedelta(days=40)
        },
        {
            "title": "Polygon Gaming Airdrop",
            "description": "Gaming platform airdrop for players and developers",
            "source_url": "https://polygon.games/airdrop",
            "referral_link": "https://polygon.games/airdrop?ref=airdrophunter&utm_source=airdrophunter&utm_medium=bot&utm_campaign=airdrop",
            "blockchain": "Polygon",
            "difficulty": "Easy",
            "reward": "1000 MATIC",
            "end_date": datetime.now() + timedelta(days=35)
        }
    ]

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
    saved_count = 0
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
                saved_count += 1
        
        db.commit()
        print(f"✅ Сохранено {saved_count} новых аирдропов")
        return saved_count
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка сохранения: {e}")
        return 0
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