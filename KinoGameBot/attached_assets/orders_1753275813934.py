from aiogram import types
from database import Database
from keyboards.inline import get_back_to_main_keyboard

db = Database()

async def my_orders(callback_query: types.CallbackQuery):
    """Show user's orders"""
    await callback_query.answer()
    
    user_id = callback_query.from_user.id
    orders = db.get_user_orders(user_id)
    
    if not orders:
        text = (
            "📦 **МОИ ЗАКАЗЫ**\n\n"
            "У вас пока нет заказов\n\n"
            "Перейдите в каталог, чтобы сделать первый заказ"
        )
    else:
        text = "📦 **МОИ ЗАКАЗЫ**\n\n"
        
        for order in orders:
            (order_id, product_key, color, quantity, total_price, 
             status, payment_status, tracking_link, created_at, product_name, delivery_address) = order
            
            # Format status
            status_emoji = {
                'pending': '⏳',
                'confirmed': '✅',
                'shipped': '📦',
                'delivered': '🎉',
                'cancelled': '❌'
            }.get(status, '❓')
            
            payment_emoji = {
                'unpaid': '💳',
                'paid': '✅',
                'refunded': '↩️'
            }.get(payment_status, '❓')
            
            color_text = f" ({color})" if color else ""
            
            text += f"**Заказ №{order_id}**\n"
            text += f"📦 {product_name}{color_text}\n"
            text += f"💰 {total_price} ₽ | {payment_emoji} {payment_status}\n"
            text += f"📍 {status_emoji} {status}\n"
            
            if tracking_link:
                text += f"🔗 [Отслеживание]({tracking_link})\n"
            
            text += f"📅 {created_at}\n\n"
    
    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_back_to_main_keyboard()
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_back_to_main_keyboard()
        )