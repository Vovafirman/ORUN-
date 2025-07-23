from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PRODUCTS
from database import Database

db = Database()

async def view_cart(callback_query: types.CallbackQuery):
    """Show user's cart"""
    await callback_query.answer()
    
    cart_items = db.get_cart(callback_query.from_user.id)
    
    if not cart_items:
        text = "🛒 **КОРЗИНА ПУСТА**\n\nВ вашей корзине пока нет товаров"
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🛍️ Перейти к покупкам", callback_data="catalog"))
        keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
        return
    
    text = "🛒 **ВАША КОРЗИНА**\n\n"
    total = 0
    
    for item in cart_items:
        # item = [id, user_id, product_key, product_name, color, price, created_at]
        text += f"📦 {item[3]} ({item[4]})\n"
        text += f"💰 {item[5]} ₽\n\n"
        total += item[5]
    
    text += f"💳 **ИТОГО: {total} ₽**"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💳 Оформить заказ", callback_data="checkout_cart"))
    keyboard.add(InlineKeyboardButton("🗑️ Очистить корзину", callback_data="clear_cart"))
    keyboard.add(InlineKeyboardButton("🛍️ Продолжить покупки", callback_data="catalog"))
    keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def clear_cart(callback_query: types.CallbackQuery):
    """Clear user's cart"""
    await callback_query.answer()
    
    db.clear_cart(callback_query.from_user.id)
    
    text = "✅ **КОРЗИНА ОЧИЩЕНА**\n\nВсе товары удалены из корзины"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🛍️ Перейти к покупкам", callback_data="catalog"))
    keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
