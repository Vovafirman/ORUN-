from aiogram import types
from database import Database
from config import CATEGORIES, PRODUCTS
from keyboards.inline import (
    get_catalog_keyboard, get_category_keyboard, get_product_keyboard, 
    get_color_keyboard, get_order_confirmation_keyboard, get_payment_keyboard,
    get_back_to_main_keyboard
)

db = Database()

async def catalog(callback_query: types.CallbackQuery):
    """Show catalog categories"""
    await callback_query.answer()

    text = (
        "🛍️ **КАТАЛОГ ТОВАРОВ**\n\n"
        "Выбери категорию:"
    )

    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_catalog_keyboard()
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_catalog_keyboard()
        )

async def show_category(callback_query: types.CallbackQuery):
    """Show products in category"""
    await callback_query.answer()

    category = callback_query.data.replace('category_', '')
    category_name = CATEGORIES.get(category, "Неизвестная категория")

    # Get products from database
    products = db.get_products_by_category(category)

    if not products:
        text = f"📦 **{category_name}**\n\nТовары в данной категории временно отсутствуют."
        try:
            await callback_query.message.edit_text(
                text, 
                parse_mode='Markdown', 
                reply_markup=get_category_keyboard(category)
            )
        except:
            await callback_query.bot.send_message(
                callback_query.message.chat.id,
                text,
                parse_mode='Markdown',
                reply_markup=get_category_keyboard(category)
            )
        return

    text = f"📦 **{category_name}**\n\n"

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for product in products:
        product_key, name, price, image = product
        text += f"• **{name}** — {price} ₽\n"
        keyboard.add(
            types.InlineKeyboardButton(
                f"{name} — {price} ₽", 
                callback_data=f"product_{product_key}"
            )
        )

    keyboard.add(
        types.InlineKeyboardButton("⬅️ Каталог", callback_data="catalog"),
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

async def show_product(callback_query: types.CallbackQuery):
    """Show product details"""
    await callback_query.answer()

    product_key = callback_query.data.replace('product_', '')
    product = db.get_product(product_key)

    if not product:
        await callback_query.message.edit_text(
            "❌ Товар не найден", 
            reply_markup=get_back_to_main_keyboard()
        )
        return

    text = f"🛍️ **{product['name']}**\n\n"
    text += f"💰 **Цена:** {product['price']} ₽\n"

    if product.get('size'):
        text += f"📏 **Размер:** {product['size']}\n"
    if product.get('density'):
        text += f"⚖️ **Плотность:** {product['density']}\n"
    if product.get('material'):
        text += f"🧵 **Материал:** {product['material']}\n"
    if product.get('description'):
        text += f"\n📝 **Описание:** {product['description']}\n"

    if product.get('colors'):
        text += f"\n🎨 **Доступные цвета:** {', '.join(product['colors'])}"

    # Send with photo if available
    if product.get('image'):
        try:
            with open(product['image'], 'rb') as photo:
                # Delete old message and send new one with photo
                await callback_query.message.delete()
                await callback_query.bot.send_photo(
                    chat_id=callback_query.message.chat.id,
                    photo=photo,
                    caption=text,
                    parse_mode='Markdown',
                    reply_markup=get_product_keyboard(product_key, product['category'])
                )
                return
        except Exception as e:
            # If image fails, continue with text
            pass

    # Send text message
    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_product_keyboard(product_key, product['category'])
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_product_keyboard(product_key, product['category'])
        )

async def select_color(callback_query: types.CallbackQuery):
    """Handle color selection"""
    await callback_query.answer()

    # Parse callback data: color_product_key_color
    parts = callback_query.data.split('_', 2)
    if len(parts) < 3:
        return

    product_key = parts[1]
    color = parts[2]

    product = db.get_product(product_key)
    if not product:
        return

    # Show options: add to cart or buy now
    text = (
        f"🎨 **{product['name']}**\n"
        f"Цвет: **{color}**\n"
        f"Цена: **{product['price']} ₽**\n\n"
        "Что хотите сделать?"
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🛒 В корзину", callback_data=f"add_cart_colored_{product_key}_{color}"),
        types.InlineKeyboardButton("💳 Купить", callback_data=f"buy_colored_{product_key}_{color}")
    )
    keyboard.add(
        types.InlineKeyboardButton("⬅️ К товару", callback_data=f"product_{product_key}"),
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

async def add_to_cart(callback_query: types.CallbackQuery):
    """Add product to cart"""
    await callback_query.answer()

    product_key = callback_query.data.replace('add_cart_', '')
    product = db.get_product(product_key)

    if not product:
        await callback_query.message.edit_text(
            "❌ Товар не найден", 
            reply_markup=get_back_to_main_keyboard()
        )
        return

    user_id = callback_query.from_user.id

    # If product has colors, show color selection
    if product.get('colors') and len(product['colors']) > 1:
        text = f"🎨 Выбери цвет для **{product['name']}**:"
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_color_keyboard(product_key, product['colors'], product['category'])
        )
        return

    # Add to cart with default color
    color = product['colors'][0] if product.get('colors') else None
    success = db.add_to_cart(user_id, product_key, color)

    if success:
        text = f"✅ **{product['name']}** добавлен в корзину!"
    else:
        text = "❌ Ошибка при добавлении в корзину"

    try:
        if callback_query.message.photo:
            # If current message has photo, delete it and send text message
            await callback_query.message.delete()
            await callback_query.bot.send_message(
                callback_query.message.chat.id,
                text,
                parse_mode='Markdown',
                reply_markup=get_back_to_main_keyboard()
            )
        else:
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

async def buy_now(callback_query: types.CallbackQuery, user_state):
    """Handle buy now"""
    await callback_query.answer()

    product_key = callback_query.data.replace('buy_now_', '')
    product = db.get_product(product_key)

    if not product:
        # Try to edit, if fails send new message
        try:
            await callback_query.message.edit_text(
                "❌ Товар не найден", 
                reply_markup=get_back_to_main_keyboard()
            )
        except:
            await callback_query.bot.send_message(
                callback_query.message.chat.id,
                "❌ Товар не найден",
                reply_markup=get_back_to_main_keyboard()
            )
        return

    # If product has multiple colors, show color selection first
    if product.get('colors') and len(product['colors']) > 1:
        text = f"🎨 Выбери цвет для **{product['name']}** перед покупкой:"
        try:
            await callback_query.message.edit_text(
                text, 
                parse_mode='Markdown', 
                reply_markup=get_color_keyboard(product_key, product['colors'], product['category'])
            )
        except:
            await callback_query.bot.send_message(
                callback_query.message.chat.id,
                text,
                parse_mode='Markdown',
                reply_markup=get_color_keyboard(product_key, product['colors'], product['category'])
            )
        return

    # Store purchase info in user state
    user_state['purchase'] = {
        'product_key': product_key,
        'color': product['colors'][0] if product.get('colors') else None
    }

    text = (
        f"📦 **Оформление заказа**\n\n"
        f"**Товар:** {product['name']}\n"
        f"**Цена:** {product['price']} ₽\n\n"
        "📍 Напиши адрес доставки:"
    )

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

async def back_to_category(callback_query: types.CallbackQuery):
    """Back to category from product"""
    await callback_query.answer()

    category = callback_query.data.replace('back_to_category_', '')

    # Simulate category callback
    new_callback = types.CallbackQuery(
        id=callback_query.id,
        from_user=callback_query.from_user,
        message=callback_query.message,
        data=f'category_{category}',
        chat_instance=callback_query.chat_instance
    )

    await show_category(new_callback)

async def handle_delivery_address(message: types.Message, user_state):
    """Handle delivery address input"""
    if 'purchase' not in user_state:
        return

    delivery_address = message.text
    user_state['purchase']['delivery_address'] = delivery_address

    product_key = user_state['purchase']['product_key']
    product = db.get_product(product_key)

    if not product:
        await message.answer("❌ Ошибка при оформлении заказа")
        return

    # Create order
    order_id = db.create_order(
        user_id=message.from_user.id,
        product_key=product_key,
        color=user_state['purchase'].get('color'),
        quantity=1,
        delivery_address=delivery_address
    )

    if not order_id:
        await message.answer("❌ Ошибка при создании заказа")
        return

    text = (
        f"📋 **Подтверждение заказа №{order_id}**\n\n"
        f"**Товар:** {product['name']}\n"
        f"**Цена:** {product['price']} ₽\n"
        f"**Адрес доставки:** {delivery_address}\n\n"
        "Подтвердить заказ?"
    )

    await message.answer(
        text, 
        parse_mode='Markdown', 
        reply_markup=get_order_confirmation_keyboard(order_id)
    )

async def confirm_order(callback_query: types.CallbackQuery, user_state):
    """Confirm order and show payment"""
    await callback_query.answer()

    order_id = callback_query.data.replace('confirm_order_', '')

    # Get order details for payment instructions
    order = db.get_order(order_id)
    if order:
        total_price = order[5]  # total_price from order

        text = (
            f"💳 **Оплата заказа №{order_id}**\n\n"
            f"💰 **Сумма к оплате: {total_price} ₽**\n\n"
            "**Способы оплаты:**\n"
            "🏦 Сбербанк: 4274 3200 1234 5678\n"
            "🥝 QIWI: +7 (900) 123-45-67\n"
            "💸 ЮMoney: 4100 1234 5678 9012\n\n"
            "📝 **В комментарии к переводу укажите:**\n"
            f"\"Заказ №{order_id}\"\n\n"
            "После оплаты нажми кнопку \"Оплачено\" ⬇️"
        )
    else:
        text = (
            f"💳 **Оплата заказа №{order_id}**\n\n"
            "После оплаты нажми кнопку \"Оплачено\""
        )

    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_payment_keyboard(order_id)
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_payment_keyboard(order_id)
        )

    # Clear purchase state
    if 'purchase' in user_state:
        del user_state['purchase']

async def payment_done(callback_query: types.CallbackQuery):
    """Handle payment confirmation"""
    await callback_query.answer()

    order_id = callback_query.data.replace('payment_done_', '')

    # Update order status to paid
    db.update_order_status(order_id, status='pending', payment_status='paid')

    # Get order details
    order = db.get_order(order_id)
    if order:
        user_id, product_key, color, quantity, total_price, status, payment_status, tracking_link, created_at, product_name, delivery_address = order[1:]

        # Notify all admins about new paid order
        from config import ADMIN_IDS
        admin_text = (
            f"🆕 **НОВЫЙ ЗАКАЗ №{order_id}**\n\n"
            f"👤 Пользователь: {callback_query.from_user.full_name} (@{callback_query.from_user.username})\n"
            f"📦 Товар: {product_name}\n"
            f"🎨 Цвет: {color or 'не указан'}\n"
            f"💰 Сумма: {total_price} ₽\n"
            f"📍 Адрес: {delivery_address}\n"
            f"💳 Статус оплаты: ✅ ОПЛАЧЕНО\n\n"
            f"⚡ Требуется обработка заказа!"
        )

        for admin_id in ADMIN_IDS:
            try:
                await callback_query.bot.send_message(
                    admin_id,
                    admin_text,
                    parse_mode='Markdown'
                )
            except:
                pass  # Skip if admin not accessible

    text = (
        f"✅ **Заказ №{order_id} принят и оплачен!**\n\n"
        "🎉 Спасибо за покупку! Администраторы уже получили уведомление о вашем заказе.\n\n"
        "📞 Мы свяжемся с вами в ближайшее время для подтверждения и отправки товара."
    )

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

async def add_cart_colored(callback_query: types.CallbackQuery):
    """Add colored product to cart"""
    await callback_query.answer()

    # Parse: add_cart_colored_product_key_color
    parts = callback_query.data.replace('add_cart_colored_', '').split('_', 1)
    if len(parts) < 2:
        return

    product_key = parts[0]
    color = parts[1]

    product = db.get_product(product_key)
    if not product:
        return

    user_id = callback_query.from_user.id
    success = db.add_to_cart(user_id, product_key, color)

    if success:
        text = f"✅ **{product['name']}** (цвет: {color}) добавлен в корзину!"
    else:
        text = "❌ Ошибка при добавлении в корзину"

    try:
        if callback_query.message.photo:
            # If current message has photo, delete it and send text message
            await callback_query.message.delete()
            await callback_query.bot.send_message(
                callback_query.message.chat.id,
                text,
                parse_mode='Markdown',
                reply_markup=get_back_to_main_keyboard()
            )
        else:
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

async def buy_colored(callback_query: types.CallbackQuery, user_state):
    """Buy colored product"""
    await callback_query.answer()

    # Parse: buy_colored_product_key_color
    parts = callback_query.data.replace('buy_colored_', '').split('_', 1)
    if len(parts) < 2:
        return

    product_key = parts[0]
    color = parts[1]

    product = db.get_product(product_key)
    if not product:
        return

    # Store purchase info in user state
    user_state['purchase'] = {
        'product_key': product_key,
        'color': color
    }

    text = (
        f"📦 **Оформление заказа**\n\n"
        f"**Товар:** {product['name']}\n"
        f"**Цвет:** {color}\n"
        f"**Цена:** {product['price']} ₽\n\n"
        "📍 Напиши адрес доставки:"
    )

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