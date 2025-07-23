import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def ensure_directory_exists(path: str):
    """Ensure directory exists, create if not"""
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Created directory: {path}")
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")

def format_price(price: float) -> str:
    """Format price for display"""
    return f"{price:.0f} ₽"

def get_status_emoji(status: str) -> str:
    """Get emoji for order status"""
    status_emojis = {
        'pending': '⏳',
        'confirmed': '✅',
        'processing': '🔄',
        'shipped': '🚚',
        'delivered': '📦',
        'cancelled': '❌'
    }
    return status_emojis.get(status, '❓')

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_price(price_str: str) -> Optional[float]:
    """Validate and convert price string to float"""
    try:
        price = float(price_str.replace(',', '.'))
        if price <= 0:
            return None
        return price
    except (ValueError, TypeError):
        return None

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    from config import ADMIN_ID
    return user_id == ADMIN_ID
