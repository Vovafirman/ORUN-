import sqlite3
import logging
from datetime import datetime
from config import DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_path = DATABASE_URL
        self.init_database()
    
    def init_database(self):
        """Initialize the database with all necessary tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                product_name TEXT,
                color TEXT,
                delivery_address TEXT,
                price INTEGER,
                status TEXT DEFAULT 'pending',
                payment_status TEXT DEFAULT 'pending',
                tracking_link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_key TEXT,
                product_name TEXT,
                color TEXT,
                price INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def add_user(self, user_id, username, first_name, last_name):
        """Add a new user to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        
        conn.commit()
        conn.close()
        logger.info(f"User {username} (ID: {user_id}) added to database")
    
    def add_to_cart(self, user_id, product_key, product_name, color, price):
        """Add item to user's cart"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cart (user_id, product_key, product_name, color, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, product_key, product_name, color, price))
        
        conn.commit()
        conn.close()
        logger.info(f"Added {product_name} ({color}) to cart for user {user_id}")
    
    def get_cart(self, user_id):
        """Get user's cart items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cart WHERE user_id = ?
        ''', (user_id,))
        
        items = cursor.fetchall()
        conn.close()
        return items
    
    def clear_cart(self, user_id):
        """Clear user's cart"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        logger.info(f"Cart cleared for user {user_id}")
    
    def create_order(self, username, product_name, color, delivery_address, price):
        """Create a new order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (username, product_name, color, delivery_address, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, product_name, color, delivery_address, price))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Order #{order_id} created for {username}")
        return order_id
    
    def get_orders(self, user_id):
        """Get user's orders by matching username from users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # First get the username for the user_id
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        user_result = cursor.fetchone()
        
        if not user_result:
            conn.close()
            return []
        
        username = user_result[0]
        
        # Then get orders for that username
        cursor.execute('''
            SELECT * FROM orders WHERE username = ? ORDER BY created_at DESC
        ''', (username,))
        
        orders = cursor.fetchall()
        conn.close()
        return orders
    
    def get_all_orders(self):
        """Get all orders for admin panel"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        orders = cursor.fetchall()
        
        conn.close()
        return orders
    
    def get_order(self, order_id):
        """Get specific order by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        
        conn.close()
        return order
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET status = ? WHERE id = ?
        ''', (status, order_id))
        
        conn.commit()
        conn.close()
        logger.info(f"Order #{order_id} status updated to {status}")
    
    def update_payment_status(self, order_id, payment_status):
        """Update payment status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET payment_status = ? WHERE id = ?
        ''', (payment_status, order_id))
        
        conn.commit()
        conn.close()
        logger.info(f"Order #{order_id} payment status updated to {payment_status}")
    
    def add_tracking_link(self, order_id, tracking_link):
        """Add tracking link to order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET tracking_link = ? WHERE id = ?
        ''', (tracking_link, order_id))
        
        conn.commit()
        conn.close()
        logger.info(f"Tracking link added to order #{order_id}")
    
    def get_stats(self):
        """Get statistics for admin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute('SELECT SUM(price) FROM orders WHERE payment_status = "paid"')
        total_revenue = cursor.fetchone()[0] or 0
        
        # Pending orders
        cursor.execute('SELECT COUNT(*) FROM orders WHERE status = "pending"')
        pending_orders = cursor.fetchone()[0]
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'total_users': total_users
        }