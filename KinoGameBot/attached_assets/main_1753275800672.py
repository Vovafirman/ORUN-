import logging
from collections import defaultdict

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import BOT_TOKEN, ADMIN_IDS
from database import Database

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

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
    confirm_payment, mark_shipped, mark_delivered, cancel_order,
    send_link
)
from handlers.help import help_menu
from keyboards.inline import get_back_to_main_keyboard, get_admin_order_keyboard


@dp.callback_query_handler(lambda c: c.data == 'help')
async def help_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = (
        "❓ **ПОМОЩЬ**\n\n"
        "Для получения помощи обратитесь к нашему оператору:\n\n"
        "👤 @PRdemon"
    )
    await callback_query.message.edit_text(message, parse_mode='Markdown', reply_markup=get_back_to_main_keyboard())


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await start(message)


@dp.message_handler(commands=['admin'])
async def handle_admin(message: types.Message):
    await admin_panel(message)


@dp.message_handler(regexp=r'^/manage_\d+$')
async def handle_manage(message: types.Message):
    await manage_order(message)


@dp.callback_query_handler(lambda c: c.data == 'open_store')
async def handle_open_store(callback_query: types.CallbackQuery):
    await open_store(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def handle_main_menu(callback_query: types.CallbackQuery):
    await main_menu(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'catalog')
async def handle_catalog(callback_query: types.CallbackQuery):
    await catalog(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('category_'))
async def handle_show_category(callback_query: types.CallbackQuery):
    await show_category(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('product_'))
async def handle_show_product(callback_query: types.CallbackQuery):
    await show_product(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('color_'))
async def handle_select_color(callback_query: types.CallbackQuery):
    await select_color(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('add_cart_colored_'))
async def handle_add_cart_colored(callback_query: types.CallbackQuery):
    await add_cart_colored(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('buy_colored_'))
async def handle_buy_colored(callback_query: types.CallbackQuery):
    await buy_colored(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query_handler(lambda c: c.data.startswith('add_cart_'))
async def handle_add_to_cart(callback_query: types.CallbackQuery):
    await add_to_cart(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('buy_now_'))
async def handle_buy_now_cb(callback_query: types.CallbackQuery):
    await buy_now(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query_handler(lambda c: c.data.startswith('back_to_category_'))
async def handle_back_to_category_cb(callback_query: types.CallbackQuery):
    await back_to_category(callback_query)


@dp.message_handler(lambda m: 'purchase' in user_states[m.from_user.id])
async def handle_delivery_address_msg(message: types.Message):
    await handle_delivery_address(message, user_states[message.from_user.id])


@dp.callback_query_handler(lambda c: c.data.startswith('confirm_order_'))
async def handle_confirm_order_cb(callback_query: types.CallbackQuery):
    await confirm_order(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query_handler(lambda c: c.data.startswith('payment_done_'))
async def handle_payment_done(callback_query: types.CallbackQuery):
    await payment_done(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'my_orders')
async def handle_my_orders(callback_query: types.CallbackQuery):
    await my_orders(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'cart')
async def handle_cart(callback_query: types.CallbackQuery):
    await view_cart(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'clear_cart')
async def handle_clear_cart(callback_query: types.CallbackQuery):
    await clear_cart(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'game')
async def handle_game(callback_query: types.CallbackQuery):
    await game(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'play_game')
async def handle_play_game(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    text = (
        "🎮 **ЗАПУСК ИГРЫ \"КИНОШЛЁП\"**\n\n"
        "Игра готова к запуску! Администратор отправит вам ссылку для отслеживания прогресса.\n\n"
        "⏳ Ожидайте ссылку от администратора..."
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
    
    # Уведомляем админов о запросе на игру
    for admin_id in ADMIN_IDS:
        try:
            admin_text = (
                f"🎮 **ЗАПРОС НА ИГРУ**\n\n"
                f"👤 Пользователь: {callback_query.from_user.id}\n"
                f"👤 Имя: {callback_query.from_user.first_name or 'Не указано'}\n"
                f"👤 Username: @{callback_query.from_user.username or 'Не указан'}\n\n"
                f"Пользователь хочет играть в \"Киношлёп\""
            )
            
            admin_keyboard = InlineKeyboardMarkup()
            admin_keyboard.add(
                InlineKeyboardButton(
                    "📤 Отправить ссылку", 
                    callback_data=f"send_game_link_{callback_query.from_user.id}"
                )
            )
            
            await callback_query.bot.send_message(
                admin_id, 
                admin_text,
                parse_mode='Markdown',
                reply_markup=admin_keyboard
            )
        except Exception as e:
            logger.error(f"Failed to notify admin {admin_id}: {e}")

@dp.callback_query_handler(lambda c: c.data == 'help')
async def handle_help(callback_query: types.CallbackQuery):
    await help_menu(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'admin_orders')
async def handle_admin_orders(callback_query: types.CallbackQuery):
    await admin_orders(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'admin_stats')
async def handle_admin_stats(callback_query: types.CallbackQuery):
    await admin_stats(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('confirm_payment_'))
async def handle_confirm_payment_cb(callback_query: types.CallbackQuery):
    await confirm_payment(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('mark_shipped_'))
async def handle_mark_shipped_cb(callback_query: types.CallbackQuery):
    await mark_shipped(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('mark_delivered_'))
async def handle_mark_delivered_cb(callback_query: types.CallbackQuery):
    await mark_delivered(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('cancel_order_'))
async def handle_cancel_order_cb(callback_query: types.CallbackQuery):
    await cancel_order(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('send_link_'))
async def handle_send_link_cb(callback_query: types.CallbackQuery):
    await send_link(callback_query, bot)

@dp.callback_query_handler(lambda c: c.data.startswith('send_game_link_'))
async def handle_send_game_link_cb(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    await callback_query.answer()
    
    user_id = callback_query.data.replace('send_game_link_', '')
    
    try:
        game_text = (
            f"🎮 **ССЫЛКА НА ИГРУ \"КИНОШЛЁП\"**\n\n"
            f"Ваша персональная ссылка для игры:\n"
            f"{GAME_URL}\n\n"
            f"🎯 Удачной игры! Покажите свои знания кино!"
        )
        
        await bot.send_message(
            user_id,
            game_text,
            parse_mode='Markdown'
        )
        
        await callback_query.message.edit_text(
            f"✅ Ссылка на игру отправлена пользователю {user_id}",
            reply_markup=get_back_to_main_keyboard()
        )
        
    except Exception as e:
        await callback_query.message.edit_text(
            f"❌ Ошибка при отправке ссылки пользователю {user_id}: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )

@dp.callback_query_handler(lambda c: c.data.startswith('manage_order_'))
async def handle_manage_order_cb(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("❌ Нет доступа")
        return
    
    order_id = callback_query.data.replace('manage_order_', '')
    
    order = db.get_order(order_id)
    
    if not order:
        await callback_query.answer("❌ Заказ не найден")
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
    
    try:
        await callback_query.message.edit_text(
            text, 
            parse_mode='Markdown', 
            reply_markup=get_admin_order_keyboard(order_id)
        )
    except:
        await callback_query.bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_admin_order_keyboard(order_id)
        )


def main():
    logger.info('Starting bot...')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()