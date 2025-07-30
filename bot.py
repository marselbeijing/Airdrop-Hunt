from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.orm import Session
from database import SessionLocal, User, Airdrop, NftBadge, encrypt_data, decrypt_data
from airdrop_parser import fetch_all_airdrops, save_airdrops_to_database
from task_executor import follow_twitter_account, join_telegram_channel, register_on_website, take_screenshot
from config import BOT_TOKEN, ADMIN_ID, FREE_USER_AIRDROP_LIMIT
import random
import string
import asyncio

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Временное хранилище для капчи: {user_id: correct_answer}
CAPTCHA_CHALLENGES = {}

def generate_captcha() -> tuple[str, str]:
    """Генерировать простую текстовую капчу"""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    question = f"{num1} + {num2} = ?"
    answer = str(num1 + num2)
    return question, answer

def check_user_limits(user_id: int) -> bool:
    """Проверить лимиты пользователя"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            return True  # Новый пользователь
        return user.daily_airdrops_count < FREE_USER_AIRDROP_LIMIT
    finally:
        db.close()

@dp.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    db = SessionLocal()
    try:
        # Проверяем, существует ли пользователь
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            # Создаем нового пользователя
            new_user = User(
                telegram_id=user_id,
                is_premium=False,
                rating=0,
                hunt_tokens=0.0
            )
            db.add(new_user)
            db.commit()
            
            welcome_text = """
🎉 Добро пожаловать в Airdrop Hunter!

🔍 Я помогу вам найти и выполнить задания для получения аирдропов.

📋 Доступные команды:
/airdrops - Показать доступные аирдропы
/do_airdrop <ID> - Выполнить задание
/leaderboard - Топ игроков
/my_tokens - Ваши токены $HUNT
/subscribe - Premium подписка

💡 Начните с команды /airdrops!
            """
        else:
            welcome_text = f"""
👋 С возвращением, {message.from_user.first_name}!

📊 Ваша статистика:
• Выполнено заданий: {user.rating}
• Токены $HUNT: {user.hunt_tokens}
• Статус: {'Premium' if user.is_premium else 'Free'}

🔍 Используйте /airdrops для поиска новых аирдропов!
            """
        
        await message.answer(welcome_text)
        
    except Exception as e:
        await message.answer("❌ Ошибка при регистрации. Попробуйте позже.")
        print(f"Ошибка при регистрации пользователя {user_id}: {e}")
    finally:
        db.close()

@dp.message(Command("airdrops"))
async def airdrops_command(message: Message):
    """Показать доступные аирдропы"""
    try:
        db = SessionLocal()
        airdrops = db.query(Airdrop).filter(Airdrop.is_moderated == True).limit(10).all()
        
        if not airdrops:
            await message.answer("📭 Пока нет доступных аирдропов. Попробуйте позже!")
            return
        
        response = "🎁 Доступные аирдропы:\n\n"
        for airdrop in airdrops:
            status_emoji = "✅" if airdrop.status == "completed" else "🆕"
            response += f"{status_emoji} <b>{airdrop.title}</b>\n"
            response += f"📝 {airdrop.description[:100]}...\n"
            response += f"💰 Награда: {airdrop.reward}\n"
            response += f"🔗 <a href='{airdrop.source_url}'>Подробнее</a>\n"
            response += f"🎯 ID: {airdrop.id}\n\n"
        
        response += "💡 Используйте /do_airdrop <ID> для выполнения задания"
        
        await message.answer(response, parse_mode="HTML", disable_web_page_preview=True)
        
    except Exception as e:
        await message.answer("❌ Ошибка при получении аирдропов")
        print(f"Ошибка при получении аирдропов: {e}")
    finally:
        db.close()

@dp.message(Command("do_airdrop"))
async def do_airdrop_command(message: Message):
    """Выполнить задание аирдропа"""
    try:
        # Парсим ID аирдропа
        args = message.text.split()
        if len(args) < 2:
            await message.answer("❌ Укажите ID аирдропа: /do_airdrop <ID>")
            return
        
        airdrop_id = int(args[1])
        user_id = message.from_user.id
        
        # Проверяем лимиты
        if not check_user_limits(user_id):
            await message.answer("⚠️ Достигнут дневной лимит заданий. Обновите до Premium!")
            return
        
        db = SessionLocal()
        try:
            airdrop = db.query(Airdrop).filter(Airdrop.id == airdrop_id).first()
            
            if not airdrop:
                await message.answer("❌ Аирдроп не найден")
                return
            
            if airdrop.status == "completed":
                await message.answer("✅ Это задание уже выполнено!")
                return
            
            # Имитация выполнения задания
            await message.answer(f"🔄 Выполняю задание: {airdrop.title}")
            
            # Выполняем задания
            tasks = []
            if "twitter" in airdrop.description.lower():
                tasks.append(follow_twitter_account("project_twitter"))
            if "telegram" in airdrop.description.lower():
                tasks.append(join_telegram_channel(airdrop.source_url))
            if "register" in airdrop.description.lower():
                tasks.append(register_on_website(airdrop.source_url))
            
            # Делаем скриншот
            screenshot_path = await take_screenshot(airdrop.source_url, f"airdrop_{airdrop_id}")
            
            # Обновляем статус
            airdrop.status = "completed"
            db.commit()
            
            # Обновляем статистику пользователя
            user = db.query(User).filter(User.telegram_id == user_id).first()
            if user:
                user.rating += 10
                user.hunt_tokens += 5.0
                user.daily_airdrops_count += 1
                db.commit()
            
            success_message = f"""
✅ Задание выполнено!

🎁 Аирдроп: {airdrop.title}
💰 Награда: {airdrop.reward}
📸 Скриншот: {screenshot_path if screenshot_path else 'Не удалось создать'}

🎯 +10 очков рейтинга
🪙 +5 токенов $HUNT

Продолжайте охотиться за аирдропами! 🚀
            """
            
            await message.answer(success_message)
            
        finally:
            db.close()
            
    except ValueError:
        await message.answer("❌ Неверный ID аирдропа")
    except Exception as e:
        await message.answer("❌ Ошибка при выполнении задания")
        print(f"Ошибка при выполнении аирдропа: {e}")

@dp.message(Command("leaderboard"))
async def leaderboard_command(message: Message):
    """Показать топ игроков"""
    try:
        db = SessionLocal()
        top_users = db.query(User).order_by(User.rating.desc()).limit(10).all()
        
        response = "🏆 Топ игроков:\n\n"
        for i, user in enumerate(top_users, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            response += f"{medal} {user.rating} очков | {user.hunt_tokens} $HUNT\n"
        
        await message.answer(response)
        
    except Exception as e:
        await message.answer("❌ Ошибка при получении рейтинга")
        print(f"Ошибка при получении рейтинга: {e}")
    finally:
        db.close()

@dp.message(Command("my_tokens"))
async def my_tokens_command(message: Message):
    """Показать токены пользователя"""
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        if user:
            response = f"""
💰 Ваши токены $HUNT: {user.hunt_tokens}

📊 Статистика:
• Рейтинг: {user.rating} очков
• Статус: {'Premium' if user.is_premium else 'Free'}
• Выполнено заданий: {user.daily_airdrops_count}/{FREE_USER_AIRDROP_LIMIT}
            """
        else:
            response = "❌ Пользователь не найден"
        
        await message.answer(response)
        
    except Exception as e:
        await message.answer("❌ Ошибка при получении токенов")
        print(f"Ошибка при получении токенов: {e}")
    finally:
        db.close()

@dp.message(Command("subscribe"))
async def subscribe_command(message: Message):
    """Premium подписка"""
    response = """
💎 Premium подписка

🚀 Преимущества:
• Неограниченное количество заданий
• Приоритетная поддержка
• Эксклюзивные аирдропы
• Бонусные токены $HUNT

💳 Стоимость: $19.99/месяц

📞 Для покупки свяжитесь с поддержкой
    """
    await message.answer(response)

# Административные команды
@dp.message(Command("parse_airdrops"))
async def parse_airdrops_command(message: Message):
    """Запустить парсинг аирдропов (только для админа)"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Доступ запрещен")
        return
    
    try:
        await message.answer("🔄 Запускаю парсинг аирдропов...")
        
        # Получаем реальные данные
        airdrops = fetch_all_airdrops()
        save_airdrops_to_database(airdrops)
        
        await message.answer(f"✅ Парсинг завершен! Добавлено {len(airdrops)} аирдропов")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при парсинге: {e}")

async def main():
    """Запуск бота"""
    print("🚀 Запуск Airdrop Hunter Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 