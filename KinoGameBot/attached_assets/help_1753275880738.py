from aiogram import types
from keyboards.inline import get_back_to_main_keyboard

async def help_menu(callback_query: types.CallbackQuery):
    """Show help information"""
    await callback_query.answer()
    
    text = (
        "❓ **ПОМОЩЬ**\n\n"
        "🛍️ **Как сделать заказ:**\n"
        "1. Выбери товар в каталоге\n"
        "2. Добавь в корзину или нажми \"Купить\"\n"
        "3. Укажи адрес доставки\n"
        "4. Подтверди заказ и оплати\n\n"
        
        "💳 **Способы оплаты:**\n"
        "• Сбербанк\n"
        "• QIWI кошелек\n"
        "• ЮMoney\n\n"
        
        "📦 **Доставка:**\n"
        "• По всей России\n"
        "• Сроки: 3-7 дней\n"
        "• Проверяйте товар при получении\n\n"
        
        "📞 **Поддержка:**\n"
        "По всем вопросам пишите администратору @admin_username"
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