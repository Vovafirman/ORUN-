from aiogram import types
from database import Database
from keyboards.inline import get_cart_keyboard, get_back_to_main_keyboard

db = Database()

async def view_cart(callback_query: types.CallbackQuery):
    """Show user's cart"""
    await callback_query.answer()
    
    user_id = callback_query.from_user.id
    cart_items = db.get_user_cart(user_id)
    
    if not cart_items:
        text = (
            "🛒 **КОРЗИНА**\n\n"
            "Корзина пуста\n\n"
            "Перейди в каталог, чтобы добавить товары"
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("🛍️ Каталог", callback_data="catalog"),
            types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        )
    else:
        text = "🛒 **КОРЗИНА**\n\n"
        total_price = 0
        
        for item in cart_items:
            product_key, color, quantity, name, price = item
            item_total = price * quantity
            total_price += item_total
            
            color_text = f" ({color})" if color else ""
            text += f"• **{name}**{color_text}\n"
            text += f"  Количество: {quantity} | Цена: {item_total} ₽\n\n"
        
        text += f"💰 **Общая сумма: {total_price} ₽**"
        keyboard = get_cart_keyboard()
    
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

async def clear_cart(callback_query: types.CallbackQuery):
    """Clear user's cart"""
    await callback_query.answer()
    
    user_id = callback_query.from_user.id
    db.clear_cart(user_id)
    
    text = "✅ Корзина очищена"
    
    try:
        await callback_query.message.edit_text(
            text, 
            reply_markup=get_back_to_main_keyboard()
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            reply_markup=get_back_to_main_keyboard()
        )