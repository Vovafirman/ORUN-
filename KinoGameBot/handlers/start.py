from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PRODUCTS, CATEGORIES
from database import Database

db = Database()

async def start(message: types.Message):
    """Handle /start command"""
    user = message.from_user

    # Register user in database
    db.add_user(user.id, user.username, user.first_name, user.last_name)

    welcome_text = (
        f"🎬 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в магазин мерча **Центр Кино**! 🎥\n\n"
        "У нас вы найдете:\n"
        "• 👕 Стильные футболки с уникальными принтами\n"
        "• 🎲 Настольные игры для любителей кино\n"
        "• 🎮 Возможность поиграть в \"Киношлёп\"\n\n"
        "Что хотите сделать?"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍️ ОТКРЫТЬ МАГАЗИН", callback_data="open_store")],
        [InlineKeyboardButton(text="🎮 ИГРАТЬ В КИНОШЛЁП", callback_data="play_game")]
    ])

    await message.answer(welcome_text, parse_mode='Markdown', reply_markup=keyboard)

async def open_store(callback_query: types.CallbackQuery):
    """Handle store opening"""
    await callback_query.answer()

    text = (
        "🏪 **МАГАЗИН МЕРЧА \"ЦЕНТР КИНО\"**\n\n"
        "Выберите, что вас интересует:"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton(text="🛒 Моя корзина", callback_data="cart")],
        [InlineKeyboardButton(text="📦 Мои заказы", callback_data="my_orders")],
        [InlineKeyboardButton(text="🎮 Играть в Киношлёп", callback_data="play_game")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])

    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def main_menu(callback_query: types.CallbackQuery):
    """Return to main menu"""
    await callback_query.answer()

    text = (
        "🏪 **МАГАЗИН МЕРЧА \"ЦЕНТР КИНО\"**\n\n"
        "Выберите, что вас интересует:"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton(text="🛒 Моя корзина", callback_data="cart")],
        [InlineKeyboardButton(text="📦 Мои заказы", callback_data="my_orders")],
        [InlineKeyboardButton(text="🎮 Играть в Киношлёп", callback_data="play_game")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])

    try:
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )