from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS
from database import Database

db = Database()

async def admin_panel(message: types.Message):
    """Show admin panel"""
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("❌ У вас нет доступа к админ-панели")
        return
    
    stats = db.get_stats()
    
    text = (
        "👨‍💼 **АДМИН-ПАНЕЛЬ**\n\n"
        f"📊 **СТАТИСТИКА:**\n"
        f"• Всего заказов: {stats['total_orders']}\n"
        f"• Ожидающих: {stats['pending_orders']}\n"
        f"• Доходы: {stats['total_revenue']} ₽\n"
        f"• Пользователей: {stats['total_users']}\n\n"
        "Выберите действие:"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📋 Все заказы", callback_data="admin_orders"))
    keyboard.add(InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"))
    
    await message.answer(text, parse_mode='Markdown', reply_markup=keyboard)

async def admin_orders(callback_query: types.CallbackQuery):
    """Show all orders for admin"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    orders = db.get_all_orders()
    
    if not orders:
        text = "📋 **ВСЕ ЗАКАЗЫ**\n\nЗаказов пока нет"
    else:
        text = "📋 **ВСЕ ЗАКАЗЫ**\n\n"
        
        for order in orders[:10]:  # Show last 10 orders
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
            
            text += f"🆔 **#{order[0]}** - @{order[1]}\n"
            text += f"📦 {order[2]} ({order[3]})\n"
            text += f"💰 {order[5]} ₽ - {status_emoji} {payment_emoji}\n"
            text += f"/manage_{order[0]}\n\n"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"))
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def admin_stats(callback_query: types.CallbackQuery):
    """Show detailed statistics"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    stats = db.get_stats()
    
    text = (
        "📊 **ДЕТАЛЬНАЯ СТАТИСТИКА**\n\n"
        f"📦 **ЗАКАЗЫ:**\n"
        f"• Всего заказов: {stats['total_orders']}\n"
        f"• Ожидающих обработки: {stats['pending_orders']}\n\n"
        f"💰 **ФИНАНСЫ:**\n"
        f"• Общий доход: {stats['total_revenue']} ₽\n\n"
        f"👥 **ПОЛЬЗОВАТЕЛИ:**\n"
        f"• Зарегистрировано: {stats['total_users']}\n"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📋 Все заказы", callback_data="admin_orders"))
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def manage_order(message: types.Message):
    """Manage specific order"""
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("❌ У вас нет доступа")
        return
    
    order_id = message.text.replace('/manage_', '')
    
    order = db.get_order(order_id)
    if not order:
        await message.reply("❌ Заказ не найден")
        return
    
    # order = [id, username, product_name, color, delivery_address, price, status, payment_status, tracking_link, created_at]
    text = (
        f"📋 **УПРАВЛЕНИЕ ЗАКАЗОМ #{order[0]}**\n\n"
        f"👤 Покупатель: @{order[1]}\n"
        f"📦 Товар: {order[2]} ({order[3]})\n"
        f"📍 Адрес: {order[4]}\n"
        f"💰 Сумма: {order[5]} ₽\n"
        f"📊 Статус: {order[6]}\n"
        f"💳 Оплата: {order[7]}\n"
        f"📅 Дата: {order[9]}\n"
    )
    
    if order[8]:  # tracking_link
        text += f"🔗 Трек: {order[8]}\n"
    
    keyboard = get_admin_order_keyboard(order_id)
    
    await message.answer(text, parse_mode='Markdown', reply_markup=keyboard)

async def confirm_payment(callback_query: types.CallbackQuery):
    """Confirm payment for order"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('confirm_payment_', '')
    db.update_payment_status(order_id, 'paid')
    
    await callback_query.answer("✅ Платеж подтвержден", show_alert=True)

async def mark_shipped(callback_query: types.CallbackQuery):
    """Mark order as shipped"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('mark_shipped_', '')
    db.update_order_status(order_id, 'shipped')
    
    await callback_query.answer("✅ Заказ отмечен как отправленный", show_alert=True)

async def mark_delivered(callback_query: types.CallbackQuery):
    """Mark order as delivered"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('mark_delivered_', '')
    db.update_order_status(order_id, 'delivered')
    
    await callback_query.answer("✅ Заказ отмечен как доставленный", show_alert=True)

async def cancel_order(callback_query: types.CallbackQuery):
    """Cancel order"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('cancel_order_', '')
    db.update_order_status(order_id, 'cancelled')
    
    await callback_query.answer("✅ Заказ отменен", show_alert=True)

async def send_link(callback_query: types.CallbackQuery, bot):
    """Send tracking link to customer"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('send_link_', '')
    
    # For demo purposes, use a sample tracking link
    tracking_link = f"https://track.example.com/{order_id}"
    
    # Add tracking link to database
    db.add_tracking_link(order_id, tracking_link)
    
    # Get order details to send to customer
    order = db.get_order(order_id)
    if order:
        customer_text = (
            f"📦 **ВАША ПОСЫЛКА ОТПРАВЛЕНА!**\n\n"
            f"Заказ #{order_id} передан в службу доставки.\n\n"
            f"🔗 Отследить посылку: {tracking_link}\n\n"
            f"Ожидайте доставку в ближайшие дни!"
        )
        
        # Here you would send to the actual customer
        # For demo, just show confirmation to admin
        await callback_query.answer("✅ Ссылка отправлена покупателю", show_alert=True)

def get_admin_order_keyboard(order_id):
    """Get keyboard for order management"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✅ Подтвердить оплату", callback_data=f"confirm_payment_{order_id}"),
        InlineKeyboardButton("🚚 Отправлен", callback_data=f"mark_shipped_{order_id}")
    )
    keyboard.add(
        InlineKeyboardButton("📦 Доставлен", callback_data=f"mark_delivered_{order_id}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_order_{order_id}")
    )
    keyboard.add(
        InlineKeyboardButton("🔗 Отправить ссылку", callback_data=f"send_link_{order_id}")
    )
    return keyboard