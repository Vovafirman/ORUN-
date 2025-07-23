from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """Main reply keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    keyboard.add(
        KeyboardButton("🛍️ Каталог"),
        KeyboardButton("🛒 Корзина")
    )
    
    keyboard.add(
        KeyboardButton("📦 Мои заказы"),
        KeyboardButton("🎮 Игра")
    )
    
    keyboard.add(
        KeyboardButton("❓ Помощь")
    )
    
    return keyboard

def get_admin_keyboard():
    """Admin reply keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    keyboard.add(
        KeyboardButton("📦 Заказы"),
        KeyboardButton("📊 Статистика")
    )
    
    keyboard.add(
        KeyboardButton("🏠 Главное меню")
    )
    
    return keyboard