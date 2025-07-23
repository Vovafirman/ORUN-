import logging
import asyncio
from collections import defaultdict

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_IDS, GAME_URL, PRODUCTS
from database import Database

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Initialize database
db = Database()

# Simple per-user state storage
user_states = defaultdict(dict)

# Import handlers after bot initialization
from handlers.start import start, open_store, main_menu
from handlers.catalog import (
    catalog, show_category, show_product, select_color,
    add_to_cart, buy_now, back_to_category, handle_delivery_address,
    confirm_order, payment_done, add_cart_colored, buy_colored
)
from handlers.cart import view_cart, clear_cart
from handlers.orders import my_orders
from handlers.game import game
from handlers.admin import (
    admin_panel, admin_orders, admin_stats, manage_order,
    confirm_payment, reject_payment, mark_shipped, mark_delivered,
    cancel_order, send_link, process_link_message, link_requests
)
from handlers.help import help_menu
from keyboards.inline import get_back_to_main_keyboard, get_admin_order_keyboard


@dp.message(Command("start"))
async def handle_start(message: types.Message):
    await start(message)


@dp.message(Command("admin"))
async def handle_admin(message: types.Message):
    await admin_panel(message)


@dp.message(F.text.regexp(r'^/manage_\d+$'))
async def handle_manage(message: types.Message):
    await manage_order(message)


@dp.callback_query(F.data == 'help')
async def help_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = (
        "❓ **ПОМОЩЬ**\n\n"
        "Для получения помощи обратитесь к нашему оператору:\n\n"
        "👤 @PRdemon"
    )
    await callback_query.message.edit_text(message, parse_mode='Markdown', reply_markup=get_back_to_main_keyboard())


@dp.callback_query(F.data == 'open_store')
async def handle_open_store(callback_query: types.CallbackQuery):
    await open_store(callback_query)


@dp.callback_query(F.data == 'main_menu')
async def handle_main_menu(callback_query: types.CallbackQuery):
    await main_menu(callback_query)


@dp.callback_query(F.data == 'catalog')
async def handle_catalog(callback_query: types.CallbackQuery):
    await catalog(callback_query)


@dp.callback_query(F.data.startswith('category_'))
async def handle_show_category(callback_query: types.CallbackQuery):
    await show_category(callback_query)


@dp.callback_query(F.data.startswith('product_'))
async def handle_show_product(callback_query: types.CallbackQuery):
    await show_product(callback_query)


@dp.callback_query(F.data.startswith('color_'))
async def handle_select_color(callback_query: types.CallbackQuery):
    await select_color(callback_query)


@dp.callback_query(F.data.startswith('cart_color_'))
async def handle_cart_color_selection(callback_query: types.CallbackQuery):
    """Handle color selection for adding to cart - FIXED"""
    await callback_query.answer()
    
    # Parse callback data: cart_color_COLOR_PRODUCT_KEY
    parts = callback_query.data.replace('cart_color_', '').split('_', 1)
    if len(parts) != 2:
        await callback_query.answer("❌ Ошибка данных", show_alert=True)
        return
    
    color, product_key = parts
    product = PRODUCTS.get(product_key)
    
    if not product:
        await callback_query.answer("❌ Товар не найден", show_alert=True)
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


@dp.callback_query(F.data.startswith('buy_color_'))
async def handle_buy_color_selection(callback_query: types.CallbackQuery):
    """Handle color selection for direct purchase - FIXED"""
    await callback_query.answer()
    
    # Parse callback data: buy_color_COLOR_PRODUCT_KEY
    parts = callback_query.data.replace('buy_color_', '').split('_', 1)
    if len(parts) != 2:
        await callback_query.answer("❌ Ошибка данных", show_alert=True)
        return
    
    color, product_key = parts
    product = PRODUCTS.get(product_key)
    
    if not product:
        await callback_query.answer("❌ Товар не найден", show_alert=True)
        return
    
    # Store purchase state
    user_states[callback_query.from_user.id]['purchase'] = {
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


@dp.callback_query(F.data.startswith('add_cart_colored_'))
async def handle_add_cart_colored(callback_query: types.CallbackQuery):
    await add_cart_colored(callback_query)


@dp.callback_query(F.data.startswith('buy_colored_'))
async def handle_buy_colored(callback_query: types.CallbackQuery):
    await buy_colored(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query(F.data.startswith('add_cart_'))
async def handle_add_to_cart(callback_query: types.CallbackQuery):
    await add_to_cart(callback_query)


@dp.callback_query(F.data.startswith('buy_now_'))
async def handle_buy_now_cb(callback_query: types.CallbackQuery):
    await buy_now(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query(F.data.startswith('back_to_category_'))
async def handle_back_to_category_cb(callback_query: types.CallbackQuery):
    await back_to_category(callback_query)


@dp.message(lambda m: 'purchase' in user_states[m.from_user.id] or 'checkout' in user_states[m.from_user.id])
async def handle_delivery_address_msg(message: types.Message):
    user_state = user_states[message.from_user.id]
    
    if 'purchase' in user_state:
        await handle_delivery_address(message, user_state)
    elif 'checkout' in user_state:
        await handle_cart_delivery_address(message, user_state)


@dp.message(lambda m: m.from_user.id in link_requests)
async def handle_admin_link_message(message: types.Message):
    await process_link_message(message, bot)


async def handle_cart_delivery_address(message: types.Message, user_state):
    """Handle delivery address for cart checkout"""
    if 'checkout' not in user_state or user_state['checkout'].get('step') != 'address':
        return
    
    address = message.text.strip()
    if len(address) < 10:
        await message.reply("❌ Пожалуйста, введите полный адрес доставки (минимум 10 символов)")
        return
    
    # Store address and show confirmation
    user_state['checkout']['address'] = address
    user_state['checkout']['step'] = 'confirm'
    
    cart_items = user_state['checkout']['items']
    total = sum(item[5] for item in cart_items)
    
    text = (
        f"📋 **ПОДТВЕРЖДЕНИЕ ЗАКАЗА**\n\n"
        f"📦 Товаров: {len(cart_items)}\n"
    )
    
    for item in cart_items:
        text += f"• {item[3]} ({item[4]}) - {item[5]} ₽\n"
    
    text += f"\n💰 Итого: {total} ₽\n"
    text += f"📍 Адрес: {address}\n\n"
    text += "Подтверждаете заказ?"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data="confirm_cart_order")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cart")]
    ])
    
    await message.answer(text, parse_mode='Markdown', reply_markup=keyboard)


@dp.callback_query(F.data.startswith('confirm_order_'))
async def handle_confirm_order_cb(callback_query: types.CallbackQuery):
    await confirm_order(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query(F.data == 'confirm_cart_order')
async def handle_confirm_cart_order(callback_query: types.CallbackQuery):
    """Confirm cart order"""
    await callback_query.answer()
    
    user_state = user_states[callback_query.from_user.id]
    
    if 'checkout' not in user_state:
        await callback_query.answer("❌ Ошибка: данные заказа не найдены", show_alert=True)
        return
    
    checkout = user_state['checkout']
    cart_items = checkout['items']
    address = checkout['address']
    
    # Create orders for each cart item
    order_ids = []
    total_amount = 0
    
    for item in cart_items:
        order_id = db.create_order(
            callback_query.from_user.username or str(callback_query.from_user.id),
            item[3],  # product_name
            item[4],  # color
            address,
            item[5]   # price
        )
        order_ids.append(order_id)
        total_amount += item[5]
    
    # Clear cart and checkout state
    db.clear_cart(callback_query.from_user.id)
    del user_state['checkout']
    
    # Notify admins
    admin_text = (
        f"🔔 **НОВЫЕ ЗАКАЗЫ**\n\n"
        f"👤 Покупатель: @{callback_query.from_user.username}\n"
        f"📦 Заказов: {len(order_ids)}\n"
        f"💰 Общая сумма: {total_amount} ₽\n"
        f"📍 Адрес: {address}\n\n"
        f"Номера заказов: {', '.join(map(str, order_ids))}\n\n"
        f"Используйте /manage_{{ID}} для управления"
    )
    
    for admin_id in ADMIN_IDS:
        try:
            await callback_query.bot.send_message(admin_id, admin_text, parse_mode='Markdown')
        except:
            pass
    
    # Show payment instructions
    text = (
        f"✅ **ЗАКАЗЫ СОЗДАНЫ!**\n\n"
        f"📦 Создано заказов: {len(order_ids)}\n"
        f"💳 **Для оплаты переведите {total_amount} ₽ на карту:**\n"
        f"5536 9138 1234 5678\n\n"
        f"📱 После оплаты нажмите кнопку ниже:"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # For simplicity, use first order ID for payment confirmation
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"payment_done_{order_ids[0]}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)


@dp.callback_query(F.data.startswith('payment_done_'))
async def handle_payment_done(callback_query: types.CallbackQuery):
    await payment_done(callback_query)


@dp.callback_query(F.data == 'my_orders')
async def handle_my_orders(callback_query: types.CallbackQuery):
    await my_orders(callback_query)


@dp.callback_query(F.data == 'cart')
async def handle_cart(callback_query: types.CallbackQuery):
    await view_cart(callback_query)


@dp.callback_query(F.data == 'clear_cart')
async def handle_clear_cart(callback_query: types.CallbackQuery):
    await clear_cart(callback_query)


@dp.callback_query(F.data == 'checkout_cart')
async def handle_checkout_cart(callback_query: types.CallbackQuery):
    """Handle cart checkout"""
    await callback_query.answer()
    
    cart_items = db.get_cart(callback_query.from_user.id)
    
    if not cart_items:
        await callback_query.answer("❌ Корзина пуста", show_alert=True)
        return
    
    # Store checkout state
    user_states[callback_query.from_user.id]['checkout'] = {
        'items': cart_items,
        'step': 'address'
    }
    
    total = sum(item[5] for item in cart_items)
    
    text = (
        f"🛒 **ОФОРМЛЕНИЕ ЗАКАЗА**\n\n"
        f"📦 Товаров в корзине: {len(cart_items)}\n"
        f"💰 Общая сумма: {total} ₽\n\n"
        "📍 Пожалуйста, введите адрес доставки:"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить заказ", callback_data="cart")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)


@dp.callback_query(F.data == 'game')
async def handle_game(callback_query: types.CallbackQuery):
    await game(callback_query)


@dp.callback_query(F.data == 'play_game')
async def handle_play_game(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    # Directly open game link
    text = (
        "🎮 **КИНОШЛЁП - ИГРАТЬ СЕЙЧАС**\n\n"
        "Игра запускается! Кликните по ссылке ниже:\n\n"
        f"[🕹️ ИГРАТЬ В КИНОШЛЁП]({GAME_URL})\n\n"
        "🎯 Удачной игры! Покажите свои знания кино!"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕹️ ИГРАТЬ СЕЙЧАС", url=GAME_URL)],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    
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


@dp.callback_query(F.data == 'admin_orders')
async def handle_admin_orders(callback_query: types.CallbackQuery):
    await admin_orders(callback_query)


@dp.callback_query(F.data == 'admin_stats')
async def handle_admin_stats(callback_query: types.CallbackQuery):
    await admin_stats(callback_query)


@dp.callback_query(F.data.startswith('confirm_payment_'))
async def handle_confirm_payment_cb(callback_query: types.CallbackQuery):
    await confirm_payment(callback_query)


@dp.callback_query(F.data.startswith('reject_payment_'))
async def handle_reject_payment_cb(callback_query: types.CallbackQuery):
    await reject_payment(callback_query)


@dp.callback_query(F.data.startswith('mark_shipped_'))
async def handle_mark_shipped_cb(callback_query: types.CallbackQuery):
    await mark_shipped(callback_query)


@dp.callback_query(F.data.startswith('mark_delivered_'))
async def handle_mark_delivered_cb(callback_query: types.CallbackQuery):
    await mark_delivered(callback_query)


@dp.callback_query(F.data.startswith('cancel_order_'))
async def handle_cancel_order_cb(callback_query: types.CallbackQuery):
    await cancel_order(callback_query)


@dp.callback_query(F.data.startswith('send_link_'))
async def handle_send_link_cb(callback_query: types.CallbackQuery):
    await send_link(callback_query, bot)


@dp.callback_query(F.data.startswith('manage_order_'))
async def handle_manage_order_cb(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    order_id = callback_query.data.replace('manage_order_', '')
    
    order = db.get_order(order_id)
    if not order:
        await callback_query.answer("❌ Заказ не найден", show_alert=True)
        return
    
    text = (
        f"📋 **УПРАВЛЕНИЕ ЗАКАЗОМ #{order_id}**\n\n"
        f"👤 Пользователь: {order[1]}\n"
        f"📦 Товар: {order[2]}\n"
        f"💰 Сумма: {order[5]} ₽\n"
        f"📊 Статус: {order[6]}\n"
        f"💳 Оплата: {order[7]}\n"
        f"📅 Дата: {order[9]}\n"
    )
    
    await callback_query.message.edit_text(
        text,
        parse_mode='Markdown',
        reply_markup=get_admin_order_keyboard(order_id)
    )


async def main():
    """Main function to start the bot"""
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
