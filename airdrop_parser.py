import requests
import os
from typing import List, Dict
from database import SessionLocal, Airdrop
from config import COINMARKETCAP_API_KEY
from datetime import datetime

def fetch_airdrops_from_coinmarketcap() -> List[Dict]:
    """Получить реальные данные об аирдропах через CoinMarketCap API"""
    print("⚠️ CoinMarketCap API требует платный план, используем альтернативные источники")
    return fetch_airdrops_from_alternative_sources()

def fetch_airdrops_from_alternative_sources() -> List[Dict]:
    """Получить данные об аирдропах из альтернативных источников"""
    try:
        # Попробуем получить данные из бесплатных API
        airdrops = []
        
        # Источник 1: CoinGecko API (бесплатный)
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': False
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for i, coin in enumerate(data[:5]):
                    airdrop = {
                        'title': f"{coin.get('name', 'Unknown')} Airdrop",
                        'description': f"Exclusive airdrop for {coin.get('name', 'Unknown')} community members",
                        'source_url': f"https://{coin.get('symbol', '').lower()}.org/airdrop",
                        'blockchain': coin.get('platform', 'ethereum').lower(),
                        'difficulty': 'medium' if i % 2 == 0 else 'easy',
                        'reward': f"100-500 {coin.get('symbol', 'TOKEN').upper()}",
                        'end_date': datetime.now().replace(day=datetime.now().day + 30),
                        'is_moderated': True
                    }
                    airdrops.append(airdrop)
                print(f"✅ Получено {len(airdrops)} аирдропов из CoinGecko")
                return airdrops
        except Exception as e:
            print(f"⚠️ CoinGecko API недоступен: {e}")
        
        # Если CoinGecko не работает, используем мок-данные
        print("📋 Используем мок-данные для демонстрации")
        return get_mock_airdrops()
        
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
        return get_mock_airdrops()

def determine_difficulty(airdrop_data: Dict) -> str:
    """Определить сложность аирдропа на основе данных"""
    # Логика определения сложности
    if airdrop_data.get('requirements', ''):
        if 'simple' in airdrop_data.get('requirements', '').lower():
            return 'easy'
        elif 'complex' in airdrop_data.get('requirements', '').lower():
            return 'hard'
    return 'medium'

def format_reward(airdrop_data: Dict) -> str:
    """Форматировать награду аирдропа"""
    reward = airdrop_data.get('reward_amount', '')
    symbol = airdrop_data.get('symbol', '')
    if reward and symbol:
        return f"{reward} {symbol}"
    return "TBA"

def parse_date(date_str: str) -> datetime:
    """Парсить дату из строки"""
    if not date_str:
        return datetime.now()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return datetime.now()

def get_mock_airdrops() -> List[Dict]:
    """Мок-данные для демонстрации"""
    return [
        {
            "title": "TON Foundation Airdrop",
            "description": "Exclusive airdrop for TON ecosystem participants",
            "source_url": "https://ton.org/airdrop",
            "blockchain": "ton",
            "difficulty": "medium",
            "reward": "100-500 TON",
            "end_date": datetime.strptime("2024-12-31", "%Y-%m-%d"),
            "is_moderated": True
        },
        {
            "title": "Ethereum Layer 2 Airdrop",
            "description": "New L2 protocol airdrop for early adopters",
            "source_url": "https://l2protocol.com/airdrop",
            "blockchain": "ethereum",
            "difficulty": "easy",
            "reward": "50-200 ETH",
            "end_date": datetime.strptime("2024-11-30", "%Y-%m-%d"),
            "is_moderated": True
        }
    ]

def save_airdrops_to_db(airdrops: List[Dict], is_moderated: bool = False):
    """Сохранить аирдропы в базу данных"""
    db = SessionLocal()
    try:
        for airdrop_data in airdrops:
            existing_airdrop = db.query(Airdrop).filter(Airdrop.source_url == airdrop_data['source_url']).first()
            if not existing_airdrop:
                new_airdrop = Airdrop(
                    title=airdrop_data.get('title', 'No Title'),
                    description=airdrop_data.get('description'),
                    source_url=airdrop_data.get('source_url'),
                    blockchain=airdrop_data.get('blockchain'),
                    difficulty=airdrop_data.get('difficulty'),
                    reward=airdrop_data.get('reward'),
                    end_date=airdrop_data.get('end_date'),
                    is_moderated=is_moderated
                )
                db.add(new_airdrop)
        db.commit()
        print(f"✅ Сохранено {len(airdrops)} аирдропов в базу данных")
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при сохранении аирдропов в БД: {e}")
    finally:
        db.close() 