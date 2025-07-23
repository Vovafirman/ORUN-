from aiogram import types
from database import Database
from keyboards.inline import get_main_menu_keyboard

db = Database()

async def start(message: types.Message):
    """Handle /start command"""
    user = message.from_user
    
    # Add user to database
    db.add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🎬 Добро пожаловать в **ЦЕНТР КИНО МЕРЧ** — официальный магазин мерча от команды YouTube канала \"Центр Кино\"!\n\n"
        "📱 Здесь ты найдешь:\n"
        "• Стильные футболки с принтами канала\n"
        "• Увлекательные настольные игры\n"
        "• Эксклюзивные товары для истинных киноманов\n\n"
        "🛍️ Выбери нужный раздел:"
    )
    
    await message.answer(text, parse_mode='Markdown', reply_markup=get_main_menu_keyboard())

async def open_store(callback_query: types.CallbackQuery):
    """Open store main menu"""
    await main_menu(callback_query)

async def main_menu(callback_query: types.CallbackQuery):
    """Show main menu"""
    await callback_query.answer()
    
    text = (
        "🎬 **ЦЕНТР КИНО МЕРЧ**\n\n"
        "🛍️ Официальный магазин мерча от команды YouTube канала \"Центр Кино\"\n\n"
        "Выбери нужный раздел:"
    )
    
    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_main_menu_keyboard()
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_main_menu_keyboard()
        )