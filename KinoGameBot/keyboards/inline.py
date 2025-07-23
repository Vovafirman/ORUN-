from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_back_to_main_keyboard():
    """Return to main menu keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    return keyboard

def get_admin_order_keyboard(order_id):
    """Get keyboard for admin order management"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"confirm_payment_{order_id}"),
            InlineKeyboardButton(text="🚚 Отправлен", callback_data=f"mark_shipped_{order_id}")
        ],
        [
            InlineKeyboardButton(text="📦 Доставлен", callback_data=f"mark_delivered_{order_id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_order_{order_id}")
        ],
        [
            InlineKeyboardButton(text="🔗 Отправить ссылку", callback_data=f"send_link_{order_id}")
        ]
    ])
    return keyboardить ссылку", callback_data=f"send_link_{order_id}")
    )
    return keyboard
