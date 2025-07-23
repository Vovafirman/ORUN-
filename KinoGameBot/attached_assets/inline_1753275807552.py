from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CATEGORIES

def get_main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    # Store and catalog buttons
    keyboard.add(
        InlineKeyboardButton("🛍️ Каталог", callback_data="catalog"),
        InlineKeyboardButton("🛒 Корзина", callback_data="cart")
    )
    
    # Orders and game
    keyboard.add(
        InlineKeyboardButton("📦 Мои заказы", callback_data="my_orders"),
        InlineKeyboardButton("🎮 Игра", callback_data="game")
    )
    
    # Help
    keyboard.add(
        InlineKeyboardButton("❓ Помощь", callback_data="help")
    )
    
    return keyboard

def get_catalog_keyboard():
    """Catalog categories keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for category_key, category_name in CATEGORIES.items():
        keyboard.add(
            InlineKeyboardButton(category_name, callback_data=f"category_{category_key}")
        )
    
    keyboard.add(
        InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu")
    )
    
    return keyboard

def get_category_keyboard(category):
    """Back to catalog keyboard"""
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(
        InlineKeyboardButton("⬅️ Каталог", callback_data="catalog"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    return keyboard

def get_product_keyboard(product_key, category):
    """Product action keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        InlineKeyboardButton("🛒 В корзину", callback_data=f"add_cart_{product_key}"),
        InlineKeyboardButton("💳 Купить", callback_data=f"buy_now_{product_key}")
    )
    
    keyboard.add(
        InlineKeyboardButton("⬅️ Назад", callback_data=f"back_to_category_{category}"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    return keyboard

def get_color_keyboard(product_key, colors, category):
    """Color selection keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for color in colors:
        keyboard.add(
            InlineKeyboardButton(color, callback_data=f"color_{product_key}_{color}")
        )
    
    keyboard.add(
        InlineKeyboardButton("⬅️ К товару", callback_data=f"product_{product_key}"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    return keyboard

def get_back_to_main_keyboard():
    """Simple back to main menu keyboard"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    return keyboard

def get_cart_keyboard():
    """Cart management keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("🗑️ Очистить корзину", callback_data="clear_cart"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    return keyboard

def get_order_confirmation_keyboard(order_id):
    """Order confirmation keyboard"""
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(
        InlineKeyboardButton("✅ Подтвердить заказ", callback_data=f"confirm_order_{order_id}"),
        InlineKeyboardButton("❌ Отменить", callback_data="main_menu")
    )
    
    return keyboard

def get_payment_keyboard(order_id):
    """Payment keyboard"""
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(
        InlineKeyboardButton("✅ Оплачено", callback_data=f"payment_done_{order_id}"),
        InlineKeyboardButton("❌ Отменить", callback_data="main_menu")
    )
    
    return keyboard

def get_admin_keyboard():
    """Admin panel keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        InlineKeyboardButton("📦 Заказы", callback_data="admin_orders"),
        InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")
    )
    
    keyboard.add(
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    return keyboard

def get_admin_order_keyboard(order_id):
    """Admin order management keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("✅ Подтвердить оплату", callback_data=f"confirm_payment_{order_id}"),
        InlineKeyboardButton("📦 Отправлено", callback_data=f"mark_shipped_{order_id}")
    )
    
    keyboard.add(
        InlineKeyboardButton("✅ Доставлено", callback_data=f"mark_delivered_{order_id}"),
        InlineKeyboardButton("🔗 Трекинг", callback_data=f"send_link_{order_id}")
    )
    
    keyboard.add(
        InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_order_{order_id}"),
        InlineKeyboardButton("⬅️ Назад", callback_data="admin_orders")
    )
    
    return keyboard