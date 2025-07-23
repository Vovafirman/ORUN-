from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import GAME_URL

async def game(callback_query: types.CallbackQuery):
    """Handle game menu - FIXED to directly open game link"""
    await callback_query.answer()
    
    # Directly show game link without extra steps
    text = (
        "🎮 **КИНОШЛЁП - ИГРАТЬ СЕЙЧАС**\n\n"
        "Добро пожаловать в увлекательную игру про кино!\n\n"
        "🎯 Проверьте свои знания киноискусства\n"
        "🏆 Соревнуйтесь с друзьями\n"
        "🎬 Откройте для себя новые фильмы\n\n"
        "Кликните на кнопку ниже, чтобы начать игру:"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🕹️ ИГРАТЬ В КИНОШЛЁП", url=GAME_URL)
    )
    keyboard.add(
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)