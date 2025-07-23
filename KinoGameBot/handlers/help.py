from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_USERNAME

async def help_menu(callback_query: types.CallbackQuery):
    """Show help information"""
    await callback_query.answer()
    
    text = (
        "❓ **ПОМОЩЬ И ПОДДЕРЖКА**\n\n"
        "Если у вас возникли вопросы или нужна помощь, "
        "обратитесь к нашему оператору:\n\n"
        f"👤 {SUPPORT_USERNAME}\n\n"
        "Мы поможем вам с:\n"
        "• Выбором товаров\n"
        "• Оформлением заказа\n"
        "• Отслеживанием доставки\n"
        "• Любыми другими вопросами"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
    
    await callback_query.message.edit_text(text, parse_mode='Markdown', reply_markup=keyboard)
