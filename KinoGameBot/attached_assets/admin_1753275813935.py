from aiogram import types
from database import Database
from config import ADMIN_IDS
from keyboards.inline import get_admin_keyboard, get_admin_order_keyboard, get_back_to_main_keyboard

db = Database()

async def admin_panel(message: types.Message):
    """Show admin panel"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет доступа к админ-панели")
        return
    
    text = (
        "👑 **АДМИН-ПАНЕЛЬ**\n\n"
        "Управление заказами и статистикой:"
    )
    
    await message.answer(
        text, 
        parse_mode='Markdown', 
        reply_markup=get_admin_keyboard()
    )

async def admin_orders(callback_query: types.CallbackQuery):
    """Show all orders for admin"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    orders = db.get_all_orders()
    
    if not orders:
        text = "📦 **ВСЕ ЗАКАЗЫ**\n\nЗаказов пока нет"
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_back_to_main_keyboard()
        )
        return
    
    text = "📦 **ВСЕ ЗАКАЗЫ**\n\n"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    for order in orders[:10]:  # Show only first 10 orders
        (order_id, user_id, product_key, color, quantity, total_price, 
         status, payment_status, tracking_link, created_at, product_name, delivery_address) = order
        
        color_text = f" ({color})" if color else ""
        order_text = f"№{order_id} | {product_name}{color_text} | {total_price}₽ | {status}"
        
        keyboard.add(
            types.InlineKeyboardButton(
                order_text, 
                callback_data=f"manage_order_{order_id}"
            )
        )
    
    keyboard.add(
        types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
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

async def admin_stats(callback_query: types.CallbackQuery):
    """Show statistics"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    orders = db.get_all_orders()
    
    total_orders = len(orders)
    total_revenue = sum(order[5] for order in orders if order[7] == 'paid')  # total_price for paid orders
    
    # Count by status
    status_counts = {}
    for order in orders:
        status = order[6]  # status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    text = (
        "📊 **СТАТИСТИКА**\n\n"
        f"📦 Всего заказов: {total_orders}\n"
        f"💰 Общая выручка: {total_revenue} ₽\n\n"
        "**По статусам:**\n"
    )
    
    for status, count in status_counts.items():
        emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'shipped': '📦',
            'delivered': '🎉',
            'cancelled': '❌'
        }.get(status, '❓')
        text += f"{emoji} {status}: {count}\n"
    
    await callback_query.message.edit_text(
        text, 
        parse_mode='Markdown', 
        reply_markup=get_back_to_main_keyboard()
    )

async def manage_order(message: types.Message):
    """Manage specific order"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа")
        return
    
    try:
        order_id = int(message.text.split('_')[-1])
    except:
        await message.answer("❌ Неверный формат команды")
        return
    
    order = db.get_order(order_id)
    
    if not order:
        await message.answer("❌ Заказ не найден")
        return
    
    (order_id, user_id, product_key, color, quantity, total_price, 
     status, payment_status, tracking_link, created_at, product_name, delivery_address) = order
    
    color_text = f" ({color})" if color else ""
    
    text = (
        f"📋 **ЗАКАЗ №{order_id}**\n\n"
        f"👤 Пользователь: {user_id}\n"
        f"📦 Товар: {product_name}{color_text}\n"
        f"💰 Сумма: {total_price} ₽\n"
        f"📍 Адрес: {delivery_address}\n"
        f"📅 Дата: {created_at}\n"
        f"📊 Статус: {status}\n"
        f"💳 Оплата: {payment_status}\n"
    )
    
    if tracking_link:
        text += f"🔗 Трекинг: {tracking_link}\n"
    
    await message.answer(
        text, 
        parse_mode='Markdown', 
        reply_markup=get_admin_order_keyboard(order_id)
    )

async def confirm_payment(callback_query: types.CallbackQuery):
    """Confirm payment"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('confirm_payment_', '')
    success = db.update_order_status(order_id, 'confirmed', 'paid')
    
    # Get order details to notify customer
    order = db.get_order(order_id)
    if success and order:
        user_id = order[1]
        product_name = order[10]
        
        # Notify customer about payment confirmation
        try:
            await callback_query.bot.send_message(
                user_id,
                f"✅ **Оплата подтверждена!**\n\n"
                f"Ваш заказ №{order_id} ({product_name}) принят в обработку.\n"
                f"📦 Скоро мы отправим его на указанный адрес!"
            )
        except:
            pass  # Skip if user not accessible
        
        text = f"✅ Оплата заказа №{order_id} подтверждена и клиент уведомлен"
    else:
        text = f"❌ Ошибка при обновлении заказа №{order_id}"
    
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

async def mark_shipped(callback_query: types.CallbackQuery):
    """Mark order as shipped"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('mark_shipped_', '')
    success = db.update_order_status(order_id, 'shipped')
    
    # Get order details to notify customer
    order = db.get_order(order_id)
    if success and order:
        user_id = order[1]
        product_name = order[10]
        
        # Notify customer about shipment
        try:
            await callback_query.bot.send_message(
                user_id,
                f"📦 **Заказ отправлен!**\n\n"
                f"Ваш заказ №{order_id} ({product_name}) отправлен!\n"
                f"🚚 Ожидайте доставку в ближайшие дни.\n\n"
                f"📞 При получении обязательно проверьте товар!"
            )
        except:
            pass
        
        text = f"📦 Заказ №{order_id} отмечен как отправленный и клиент уведомлен"
    else:
        text = f"❌ Ошибка при обновлении заказа №{order_id}"
    
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

async def mark_delivered(callback_query: types.CallbackQuery):
    """Mark order as delivered"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('mark_delivered_', '')
    success = db.update_order_status(order_id, 'delivered')
    
    # Get order details to notify customer
    order = db.get_order(order_id)
    if success and order:
        user_id = order[1]
        product_name = order[10]
        
        # Notify customer about delivery
        try:
            await callback_query.bot.send_message(
                user_id,
                f"🎉 **Заказ доставлен!**\n\n"
                f"Ваш заказ №{order_id} ({product_name}) успешно доставлен!\n\n"
                f"🙏 Спасибо за покупку в ЦЕНТР КИНО МЕРЧ!\n"
                f"⭐ Оставьте отзыв о товаре, если довольны покупкой."
            )
        except:
            pass
        
        text = f"🎉 Заказ №{order_id} отмечен как доставленный и клиент уведомлен"
    else:
        text = f"❌ Ошибка при обновлении заказа №{order_id}"
    
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

async def cancel_order(callback_query: types.CallbackQuery):
    """Cancel order"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('cancel_order_', '')
    success = db.update_order_status(order_id, 'cancelled')
    
    if success:
        text = f"❌ Заказ №{order_id} отменен"
    else:
        text = f"❌ Ошибка при обновлении заказа №{order_id}"
    
    await callback_query.message.edit_text(
        text, 
        reply_markup=get_back_to_main_keyboard()
    )

async def send_link(callback_query: types.CallbackQuery, bot):
    """Send tracking link"""
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('send_link_', '')
    order = db.get_order(order_id)
    
    if not order:
        await callback_query.message.edit_text(
            "❌ Заказ не найден", 
            reply_markup=get_back_to_main_keyboard()
        )
        return
    
    user_id = order[1]  # user_id from order
    
    try:
        await bot.send_message(
            user_id,
            f"🔗 Ссылка для отслеживания заказа №{order_id}:\nhttps://example.com/track/{order_id}"
        )
        text = f"✅ Ссылка отправлена пользователю для заказа №{order_id}"
    except:
        text = f"❌ Не удалось отправить ссылку пользователю для заказа №{order_id}"
    
    await callback_query.message.edit_text(
        text, 
        reply_markup=get_back_to_main_keyboard()
    )