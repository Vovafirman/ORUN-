from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата в главное меню."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    return keyboard


def get_admin_order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Клавиатура управления заказом для администраторов."""
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
    return keyboard

