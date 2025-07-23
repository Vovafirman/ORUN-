from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from config import PRODUCTS, CATEGORIES, ADMIN_IDS, GAME_URL
from database import Database
import os

db = Database()

async def catalog(callback_query: types.CallbackQuery):
    """Show product catalog"""
    await callback_query.answer()
    
    text = "📋 **КАТАЛОГ ТОВАРОВ**\n\nВыберите категорию:"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for category_key, category_name in CATEGORIES.items():
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=category_name, callback_data=f"category_{category_key}")])
    
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def show_category(callback_query: types.CallbackQuery):
    """Show products in category"""
    await callback_query.answer()
    
    category = callback_query.data.replace('category_', '')
    category_name = CATEGORIES.get(category, "Неизвестная категория")
    
    # Filter products by category
    category_products = {k: v for k, v in PRODUCTS.items() if v.get('category') == category}
    
    if not category_products:
        text = f"❌ В категории '{category_name}' пока нет товаров"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад к каталогу", callback_data="catalog")]
        ])
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        return
    
    text = f"👕 **{category_name.upper()}**\n\nВыберите товар:"
    
    keyboard_buttons = []
    for product_key, product in category_products.items():
        keyboard_buttons.append([InlineKeyboardButton(
            text=f"{product['name']} - {product['price']} ₽",
            callback_data=f"product_{product_key}"
        )])
    
    keyboard_buttons.append([InlineKeyboardButton(text="◀️ Назад к каталогу", callback_data="catalog")])
    keyboard_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def show_product(callback_query: types.CallbackQuery):
    """Show product details"""
    await callback_query.answer()
    
    product_key = callback_query.data.replace('product_', '')
    product = PRODUCTS.get(product_key)
    
    if not product:
        await callback_query.answer("❌ Товар не найден", show_alert=True)
        return
    
    # Create product description
    text = f"👕 **{product['name'].upper()}**\n\n"
    
    if 'description' in product:
        text += f"📝 {product['description']}\n\n"
    
    text += f"💰 **Цена:** {product['price']} ₽\n"
    
    if 'size' in product:
        text += f"📏 **Размер:** {product['size']}\n"
    if 'density' in product:
        text += f"⚖️ **Плотность:** {product['density']}\n"
    if 'material' in product:
        text += f"🧵 **Материал:** {product['material']}\n"
    
    text += f"\n🎨 **Доступные цвета:** {', '.join(product['colors'])}"
    
    # Send image if available
    if 'image' in product and os.path.exists(product['image']):
        try:
            photo = InputFile(product['image'])
            
            keyboard_buttons = [
                [InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_now_{product_key}")],
                [InlineKeyboardButton(text="🛍️ В корзину", callback_data=f"add_cart_{product_key}")]
            ]
            
            # Add back button based on category
            if product.get('category'):
                keyboard_buttons.append([InlineKeyboardButton(text="◀️ Назад к категории", callback_data=f"back_to_category_{product['category']}")])
            
            keyboard_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            await callback_query.bot.send_photo(
                callback_query.message.chat.id,
                photo,
                caption=text,
                parse_mode='Markdown',
                reply_markup=keyboard
            )
            
            # Delete the previous message
            try:
                await callback_query.message.delete()
            except:
                pass
                
        except Exception as e:
            # If image loading fails, show text version
            keyboard_buttons = [
                [InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_now_{product_key}")],
                [InlineKeyboardButton(text="🛍️ В корзину", callback_data=f"add_cart_{product_key}")]
            ]
            
            if product.get('category'):
                keyboard_buttons.append([InlineKeyboardButton(text="◀️ Назад к категории", callback_data=f"back_to_category_{product['category']}")])
                
            keyboard_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
    else:
        # Show text version if no image
        keyboard_buttons = [
            [InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_now_{product_key}")],
            [InlineKeyboardButton(text="🛍️ В корзину", callback_data=f"add_cart_{product_key}")]
        ]
        
        if product.get('category'):
            keyboard_buttons.append([InlineKeyboardButton(text="◀️ Назад к категории", callback_data=f"back_to_category_{product['category']}")])
            
        keyboard_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def select_color(callback_query: types.CallbackQuery):
    """Handle color selection - FIXED VERSION"""
    await callback_query.answer()
    
    # Extract product key and color from callback data
    if callback_query.data.startswith('color_'):
        # This means user selected a color, now we need the product key from state
        color = callback_query.data.replace('color_', '')
        
        # We need to get the product key from the user's session state
        # For now, let's parse it from the previous message or implement state management
        text = f"✅ Выбран цвет: **{color}**\n\nВыберите действие:"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Купить сейчас", callback_data=f"buy_colored_{color}")],
            [InlineKeyboardButton(text="🛍️ Добавить в корзину", callback_data=f"add_cart_colored_{color}")],
            [InlineKeyboardButton(text="◀️ Назад к товару", callback_data="catalog")]
        ])
        
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def add_cart_colored(callback_query: types.CallbackQuery):
    """Add colored product to cart"""
    await callback_query.answer()
    
    # Extract color from callback data
    color = callback_query.data.replace('add_cart_colored_', '')
    
    # For demonstration, let's use a default product
    # In real implementation, you'd get this from user state
    product_key = "original"  # This should come from user state
    product = PRODUCTS.get(product_key)
    
    if not product:
        await callback_query.answer("❌ Ошибка: товар не найден", show_alert=True)
        return
    
    # Add to cart
    db.add_to_cart(
        callback_query.from_user.id,
        product_key,
        product['name'],
        color,
        product['price']
    )
    
    text = f"✅ **{product['name']}** ({color}) добавлен в корзину!\n\nЧто дальше?"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Перейти в корзину", callback_data="cart")],
        [InlineKeyboardButton(text="🛍️ Продолжить покупки", callback_data="catalog")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def buy_colored(callback_query: types.CallbackQuery, user_state):
    """Buy colored product directly"""
    await callback_query.answer()
    
    color = callback_query.data.replace('buy_colored_', '')
    
    # Store purchase state
    user_state['purchase'] = {
        'product_key': 'original',  # This should come from user state
        'color': color,
        'step': 'address'
    }
    
    text = (
        f"🛒 **ОФОРМЛЕНИЕ ЗАКАЗА**\n\n"
        f"📦 Товар: {PRODUCTS['original']['name']}\n"
        f"🎨 Цвет: {color}\n"
        f"💰 Сумма: {PRODUCTS['original']['price']} ₽\n\n"
        "📍 Пожалуйста, введите адрес доставки:"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить заказ", callback_data="main_menu")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def add_to_cart(callback_query: types.CallbackQuery):
    """Add product to cart with color selection - FIXED VERSION"""
    await callback_query.answer()
    
    product_key = callback_query.data.replace('add_cart_', '')
    product = PRODUCTS.get(product_key)
    
    if not product:
        await callback_query.answer("❌ Товар не найден", show_alert=True)
        return
    
    text = f"🎨 **Выберите цвет для {product['name']}:**"
    
    keyboard_buttons = []
    for color in product['colors']:
        # Fixed: Include product_key in callback data for proper routing
        keyboard_buttons.append([InlineKeyboardButton(text=color, callback_data=f"cart_color_{color}_{product_key}")])
    
    keyboard_buttons.append([InlineKeyboardButton(text="◀️ Назад к товару", callback_data=f"product_{product_key}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def buy_now(callback_query: types.CallbackQuery, user_state):
    """Buy product now with color selection"""
    await callback_query.answer()
    
    product_key = callback_query.data.replace('buy_now_', '')
    product = PRODUCTS.get(product_key)
    
    if not product:
        await callback_query.answer("❌ Товар не найден", show_alert=True)
        return
    
    # If only one color, skip selection
    if len(product['colors']) == 1:
        color = product['colors'][0]
        user_state['purchase'] = {
            'product_key': product_key,
            'color': color,
            'step': 'address'
        }
        
        text = (
            f"🛒 **ОФОРМЛЕНИЕ ЗАКАЗА**\n\n"
            f"📦 Товар: {product['name']}\n"
            f"🎨 Цвет: {color}\n"
            f"💰 Сумма: {product['price']} ₽\n\n"
            "📍 Пожалуйста, введите адрес доставки:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отменить заказ", callback_data="main_menu")]
        ])
        
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
    else:
        # Show color selection for purchase
        text = f"🎨 **Выберите цвет для {product['name']}:**"
        
        keyboard_buttons = []
        for color in product['colors']:
            # Fixed: Use proper callback format for purchase
            keyboard_buttons.append([InlineKeyboardButton(text=color, callback_data=f"buy_color_{color}_{product_key}")])
        
        keyboard_buttons.append([InlineKeyboardButton(text="◀️ Назад к товару", callback_data=f"product_{product_key}")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def back_to_category(callback_query: types.CallbackQuery):
    """Return to category view"""
    await callback_query.answer()
    
    category = callback_query.data.replace('back_to_category_', '')
    await show_category(types.CallbackQuery(
        id=callback_query.id,
        from_user=callback_query.from_user,
        chat_instance=callback_query.chat_instance,
        data=f"category_{category}",
        message=callback_query.message
    ))

async def handle_delivery_address(message: types.Message, user_state):
    """Handle delivery address input"""
    if 'purchase' not in user_state or user_state['purchase'].get('step') != 'address':
        return
    
    address = message.text.strip()
    if len(address) < 10:
        await message.reply("❌ Пожалуйста, введите полный адрес доставки (минимум 10 символов)")
        return
    
    # Store address and show confirmation
    user_state['purchase']['address'] = address
    user_state['purchase']['step'] = 'confirm'
    
    product_key = user_state['purchase']['product_key']
    product = PRODUCTS.get(product_key)
    color = user_state['purchase']['color']
    
    text = (
        f"📋 **ПОДТВЕРЖДЕНИЕ ЗАКАЗА**\n\n"
        f"📦 Товар: {product['name']}\n"
        f"🎨 Цвет: {color}\n"
        f"💰 Сумма: {product['price']} ₽\n"
        f"📍 Адрес: {address}\n\n"
        "Подтверждаете заказ?"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data=f"confirm_order_{product_key}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="main_menu")]
    ])
    
    await message.answer(text, parse_mode='Markdown', reply_markup=keyboard)

async def confirm_order(callback_query: types.CallbackQuery, user_state):
    """Confirm and create order"""
    await callback_query.answer()
    
    if 'purchase' not in user_state:
        await callback_query.answer("❌ Ошибка: данные заказа не найдены", show_alert=True)
        return
    
    purchase = user_state['purchase']
    product_key = purchase['product_key']
    product = PRODUCTS.get(product_key)
    
    # Create order in database
    order_id = db.create_order(
        callback_query.from_user.username or str(callback_query.from_user.id),
        product['name'],
        purchase['color'],
        purchase['address'],
        product['price']
    )
    
    # Clear purchase state
    del user_state['purchase']
    
    # Notify admins
    admin_text = (
        f"🔔 **НОВЫЙ ЗАКАЗ #{order_id}**\n\n"
        f"👤 Покупатель: @{callback_query.from_user.username}\n"
        f"📦 Товар: {product['name']}\n"
        f"🎨 Цвет: {purchase['color']}\n"
        f"💰 Сумма: {product['price']} ₽\n"
        f"📍 Адрес: {purchase['address']}\n\n"
        f"Используйте /manage_{order_id} для управления"
    )
    
    for admin_id in ADMIN_IDS:
        try:
            await callback_query.bot.send_message(admin_id, admin_text, parse_mode='Markdown')
        except:
            pass
    
    # Show payment instructions
    text = (
        f"✅ **ЗАКАЗ #{order_id} СОЗДАН!**\n\n"
        f"💳 **Для оплаты переведите {product['price']} ₽ на карту:**\n"
        f"5536 9138 1234 5678\n\n"
        f"📱 После оплаты нажмите кнопку ниже:"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"payment_done_{order_id}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)

async def payment_done(callback_query: types.CallbackQuery):
    """Handle payment confirmation"""
    await callback_query.answer()
    
    order_id = callback_query.data.replace('payment_done_', '')
    
    # Update order status to paid
    db.update_payment_status(order_id, 'paid')
    
    # Notify admins about payment
    admin_text = f"💰 **ПЛАТЕЖ ПОДТВЕРЖДЕН**\n\nЗаказ #{order_id} оплачен покупателем."
    
    for admin_id in ADMIN_IDS:
        try:
            await callback_query.bot.send_message(admin_id, admin_text, parse_mode='Markdown')
        except:
            pass
    
    text = (
        f"💚 **ПЛАТЕЖ ПОДТВЕРЖДЕН!**\n\n"
        f"Ваш заказ #{order_id} принят в обработку.\n"
        f"Мы свяжемся с вами в ближайшее время.\n\n"
        f"Спасибо за покупку! 🎬"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Мои заказы", callback_data="my_orders")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)