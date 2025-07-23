"""
Helper functions for the bot
"""

def format_price(price):
    """Format price with ruble symbol"""
    return f"{price} ₽"

def format_order_status(status):
    """Format order status with emoji"""
    status_map = {
        'pending': '⏳ Ожидает',
        'processing': '🔄 В обработке',
        'shipped': '🚚 Отправлен',
        'delivered': '✅ Доставлен',
        'cancelled': '❌ Отменен'
    }
    return status_map.get(status, f'❓ {status}')

def format_payment_status(status):
    """Format payment status with emoji"""
    status_map = {
        'pending': '⏳ Ожидает',
        'paid': '✅ Оплачен',
        'failed': '❌ Ошибка'
    }
    return status_map.get(status, f'❓ {status}')