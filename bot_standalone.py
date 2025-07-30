#!/usr/bin/env python3
"""
Standalone Telegram Bot for Airdrop Hunter
Запускается отдельно от веб-приложения
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMIN_ID
from database import SessionLocal, User, Airdrop
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Клавиатуры
def get_main_keyboard():
    """Главная клавиатура"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Найти аирдропы", callback_data="search_airdrops"),
            InlineKeyboardButton(text="📊 Моя статистика", callback_data="my_stats")
        ],
        [
            InlineKeyboardButton(text="🏆 Рейтинг", callback_data="leaderboard"),
            InlineKeyboardButton(text="💰 Заработок", callback_data="earnings")
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"),
            InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")
        ]
    ])
    return keyboard

def get_airdrops_keyboard():
    """Клавиатура для аирдропов"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🆕 Новые аирдропы", callback_data="new_airdrops"),
            InlineKeyboardButton(text="🔥 Популярные", callback_data="popular_airdrops")
        ],
        [
            InlineKeyboardButton(text="💰 Высокие награды", callback_data="high_rewards"),
            InlineKeyboardButton(text="⚡ Быстрые", callback_data="quick_airdrops")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
        ]
    ])
    return keyboard

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Регистрируем пользователя
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            user = User(
                telegram_id=user_id,
                username=username,
                daily_airdrops_count=0,
                last_airdrop_date=None
            )
            db.add(user)
            db.commit()
            welcome_text = f"🎉 Добро пожаловать в Airdrop Hunter, {username}!\n\n"
        else:
            welcome_text = f"👋 С возвращением, {username}!\n\n"
    finally:
        db.close()
    
    welcome_text += (
        "🚀 Я помогу вам найти и участвовать в лучших криптовалютных аирдропах!\n\n"
        "📱 Используйте кнопки ниже для навигации:\n"
        "• 🔍 Найти аирдропы - поиск новых возможностей\n"
        "• 📊 Моя статистика - ваш прогресс\n"
        "• 🏆 Рейтинг - сравнение с другими\n"
        "• 💰 Заработок - ваши награды\n"
        "• ⚙️ Настройки - персонализация\n"
        "• ℹ️ Помощь - инструкции"
    )
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "📚 **Справка по командам:**\n\n"
        "/start - Запустить бота\n"
        "/help - Показать эту справку\n"
        "/search - Найти аирдропы\n"
        "/stats - Ваша статистика\n"
        "/ranking - Рейтинг пользователей\n"
        "/settings - Настройки\n\n"
        "💡 **Советы:**\n"
        "• Используйте кнопки для быстрой навигации\n"
        "• Регулярно проверяйте новые аирдропы\n"
        "• Выполняйте задания для увеличения наград\n"
        "• Приглашайте друзей для бонусов"
    )
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    """Обработчик команды /search"""
    await message.answer(
        "🔍 **Поиск аирдропов**\n\n"
        "Выберите тип аирдропов для поиска:",
        reply_markup=get_airdrops_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """Обработчик команды /stats"""
    user_id = message.from_user.id
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user:
            stats_text = (
                f"📊 **Ваша статистика**\n\n"
                f"👤 Пользователь: @{message.from_user.username or 'Не указан'}\n"
                f"📅 Дата регистрации: {user.created_at.strftime('%d.%m.%Y')}\n"
                f"🎯 Найденных аирдропов: {user.daily_airdrops_count}\n"
                f"💰 Общий заработок: $0 (пока не реализовано)\n"
                f"🏆 Уровень: Новичок\n"
                f"🔥 Дней подряд: 1"
            )
        else:
            stats_text = "❌ Статистика не найдена. Используйте /start для регистрации."
    finally:
        db.close()
    
    await message.answer(stats_text, parse_mode="Markdown")

# Обработчики callback-запросов
@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    """Обработчик всех callback-запросов"""
    if callback.data == "search_airdrops":
        await callback.message.edit_text(
            "🔍 **Поиск аирдропов**\n\n"
            "Выберите тип аирдропов для поиска:",
            reply_markup=get_airdrops_keyboard(),
            parse_mode="Markdown"
        )
    
    elif callback.data == "my_stats":
        user_id = callback.from_user.id
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == user_id).first()
            if user:
                stats_text = (
                    f"📊 **Ваша статистика**\n\n"
                    f"👤 Пользователь: @{callback.from_user.username or 'Не указан'}\n"
                    f"📅 Дата регистрации: {user.created_at.strftime('%d.%m.%Y')}\n"
                    f"🎯 Найденных аирдропов: {user.daily_airdrops_count}\n"
                    f"💰 Общий заработок: $0 (пока не реализовано)\n"
                    f"🏆 Уровень: Новичок\n"
                    f"🔥 Дней подряд: 1"
                )
            else:
                stats_text = "❌ Статистика не найдена. Используйте /start для регистрации."
        finally:
            db.close()
        
        await callback.message.edit_text(stats_text, parse_mode="Markdown")
    
    elif callback.data == "leaderboard":
        await callback.message.edit_text(
            "🏆 **Рейтинг пользователей**\n\n"
            "📊 Топ-10 охотников за аирдропами:\n\n"
            "🥇 @user1 - $2,847\n"
            "🥈 @user2 - $1,923\n"
            "🥉 @user3 - $1,456\n"
            "4️⃣ @user4 - $1,234\n"
            "5️⃣ @user5 - $987\n\n"
            "💡 Продолжайте участвовать, чтобы подняться в рейтинге!",
            parse_mode="Markdown"
        )
    
    elif callback.data == "earnings":
        await callback.message.edit_text(
            "💰 **Ваш заработок**\n\n"
            "📈 Общая статистика:\n"
            "• Общий заработок: $0\n"
            "• За этот месяц: $0\n"
            "• За эту неделю: $0\n"
            "• Сегодня: $0\n\n"
            "🎯 Цель: $100\n"
            "📊 Прогресс: 0%\n\n"
            "💡 Участвуйте в аирдропах для увеличения заработка!",
            parse_mode="Markdown"
        )
    
    elif callback.data == "settings":
        await callback.message.edit_text(
            "⚙️ **Настройки**\n\n"
            "🔔 Уведомления:\n"
            "• Новые аирдропы: ✅\n"
            "• Напоминания: ✅\n"
            "• Рейтинг: ✅\n\n"
            "🌍 Язык: Русский\n"
            "💰 Валюта: USD\n"
            "⏰ Часовой пояс: UTC+3\n\n"
            "💡 Настройки пока не редактируются",
            parse_mode="Markdown"
        )
    
    elif callback.data == "help":
        help_text = (
            "📚 **Справка**\n\n"
            "🔍 **Поиск аирдропов:**\n"
            "• Используйте кнопку 'Найти аирдропы'\n"
            "• Выбирайте по категориям\n"
            "• Следите за новыми поступлениями\n\n"
            "📊 **Статистика:**\n"
            "• Отслеживайте свой прогресс\n"
            "• Смотрите заработок\n"
            "• Сравнивайте с другими\n\n"
            "🏆 **Рейтинг:**\n"
            "• Соревнуйтесь с другими\n"
            "• Получайте бонусы за активность\n"
            "• Достигайте новых уровней\n\n"
            "💡 **Советы:**\n"
            "• Регулярно проверяйте новые аирдропы\n"
            "• Выполняйте все задания\n"
            "• Приглашайте друзей"
        )
        await callback.message.edit_text(help_text, parse_mode="Markdown")
    
    elif callback.data == "main_menu":
        await callback.message.edit_text(
            "🏠 **Главное меню**\n\n"
            "🚀 Добро пожаловать в Airdrop Hunter!\n\n"
            "📱 Используйте кнопки ниже для навигации:",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    
    elif callback.data in ["new_airdrops", "popular_airdrops", "high_rewards", "quick_airdrops"]:
        # Имитация поиска аирдропов
        airdrops = [
            {
                "title": "TON Foundation Airdrop",
                "reward": "100-500 TON",
                "difficulty": "Средняя",
                "end_date": "31.12.2024"
            },
            {
                "title": "Ethereum Layer 2 Airdrop",
                "reward": "50-200 ETH",
                "difficulty": "Легкая",
                "end_date": "30.11.2024"
            },
            {
                "title": "Solana DeFi Airdrop",
                "reward": "1000-5000 SOL",
                "difficulty": "Сложная",
                "end_date": "31.10.2024"
            }
        ]
        
        airdrops_text = "🎯 **Найденные аирдропы:**\n\n"
        for i, airdrop in enumerate(airdrops, 1):
            airdrops_text += (
                f"{i}. **{airdrop['title']}**\n"
                f"💰 Награда: {airdrop['reward']}\n"
                f"⚡ Сложность: {airdrop['difficulty']}\n"
                f"📅 До: {airdrop['end_date']}\n\n"
            )
        
        airdrops_text += "💡 Нажмите на аирдроп для подробностей"
        
        await callback.message.edit_text(
            airdrops_text,
            parse_mode="Markdown"
        )
    
    await callback.answer()

async def main():
    """Главная функция"""
    logger.info("🚀 Запуск Telegram бота Airdrop Hunter...")
    
    # Инициализация базы данных
    from database import init_db
    init_db()
    
    # Запуск бота
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main()) 