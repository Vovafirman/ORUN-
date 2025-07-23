from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import GAME_URL
from keyboards.inline import get_back_to_main_keyboard

async def game(callback_query: types.CallbackQuery):
    """Show game information"""
    await callback_query.answer()
    
    text = (
        "🎮 **ИГРА \"КИНОШЛЁП\"**\n\n"
        "Увлекательная онлайн-игра для истинных киноманов!\n\n"
        "🎯 Угадывай фильмы по кадрам\n"
        "🏆 Соревнуйся с друзьями\n"
        "🎪 Проверь свои знания кино\n\n"
        "Нажми кнопку ниже, чтобы начать играть!"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🕹️ ИГРАТЬ СЕЙЧАС", callback_data="play_game")
    )
    keyboard.add(
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
