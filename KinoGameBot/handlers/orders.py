from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Database

db = Database()

async def my_orders(callback_query: types.CallbackQuery):
    """Show user's orders"""
    await callback_query.answer()
    
    orders = db.get_orders(callback_query.from_user.id)
    
    if not orders:
        text = "📦 **МОИ ЗАКАЗЫ**\n\nУ вас пока нет заказов"
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🛍️ Перейти к покупкам", callback_data="catalog"))
        keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
        return
    
    text = "📦 **МОИ ЗАКАЗЫ**\n\n"
    
    for order in orders:
        # order = [id, username, product_name, color, delivery_address, price, status, payment_status, tracking_link, created_at]
        status_emoji = {
            'pending': '⏳',
            'processing': '🔄', 
            'shipped': '🚚',
            'delivered': '✅',
            'cancelled': '❌'
        }.get(order[6], '❓')
        
        payment_emoji = {
            'pending': '⏳',
            'paid': '✅',
            'failed': '❌'
        }.get(order[7], '❓')
        
        text += f"🆔 **Заказ #{order[0]}**\n"
        text += f"📦 {order[2]} ({order[3]})\n"
        text += f"💰 {order[5]} ₽\n"
        text += f"📊 Статус: {status_emoji} {order[6]}\n"
        text += f"💳 Оплата: {payment_emoji} {order[7]}\n"
        
        if order[8]:  # tracking_link
            text += f"🔗 [Отследить посылку]({order[8]})\n"
        
        text += f"📅 {order[9]}\n\n"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🛍️ Сделать новый заказ", callback_data="catalog"))
    keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
