import sqlite3
import logging
from datetime import datetime
from config import DATABASE_URL, PRODUCTS

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.init_db()
        self.populate_products()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(DATABASE_URL)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_key TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    size TEXT,
                    density TEXT,
                    material TEXT,
                    description TEXT,
                    image TEXT,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Product colors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_colors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_key TEXT NOT NULL,
                    color TEXT NOT NULL,
                    FOREIGN KEY (product_key) REFERENCES products (product_key)
                )
            """)
            
            # Orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_key TEXT NOT NULL,
                    color TEXT,
                    quantity INTEGER DEFAULT 1,
                    total_price INTEGER NOT NULL,
                    delivery_address TEXT,
                    status TEXT DEFAULT 'pending',
                    payment_status TEXT DEFAULT 'unpaid',
                    tracking_link TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (product_key) REFERENCES products (product_key)
                )
            """)
            
            # Cart table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_key TEXT NOT NULL,
                    color TEXT,
                    quantity INTEGER DEFAULT 1,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (product_key) REFERENCES products (product_key)
                )
            """)
            
            conn.commit()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def populate_products(self):
        """Populate products from config"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            for product_key, product_data in PRODUCTS.items():
                # Insert or update product
                cursor.execute("""
                    INSERT OR REPLACE INTO products 
                    (product_key, name, category, price, size, density, material, description, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    product_key,
                    product_data["name"],
                    product_data["category"],
                    product_data["price"],
                    product_data.get("size"),
                    product_data.get("density"),
                    product_data.get("material"),
                    product_data.get("description"),
                    product_data.get("image")
                ))
                
                # Clear and insert colors
                cursor.execute("DELETE FROM product_colors WHERE product_key = ?", (product_key,))
                
                if "colors" in product_data:
                    for color in product_data["colors"]:
                        cursor.execute("""
                            INSERT INTO product_colors (product_key, color)
                            VALUES (?, ?)
                        """, (product_key, color))
            
            conn.commit()
            logger.info("Products populated successfully")
            
        except Exception as e:
            logger.error(f"Error populating products: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def add_user(self, telegram_id, username=None, first_name=None, last_name=None):
        """Add or update user"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users 
                (telegram_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            """, (telegram_id, username, first_name, last_name))
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error adding user: {e}")
        finally:
            conn.close()
    
    def get_products_by_category(self, category):
        """Get all products by category"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT product_key, name, price, image 
                FROM products 
                WHERE category = ? AND is_active = 1
                ORDER BY name
            """, (category,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting products by category: {e}")
            return []
        finally:
            conn.close()
    
    def get_product(self, product_key):
        """Get product by key"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM products WHERE product_key = ? AND is_active = 1
            """, (product_key,))
            product = cursor.fetchone()
            
            if product:
                # Get colors for this product
                cursor.execute("""
                    SELECT color FROM product_colors WHERE product_key = ?
                """, (product_key,))
                colors = [row[0] for row in cursor.fetchall()]
                
                return {
                    'product_key': product[1],
                    'name': product[2],
                    'category': product[3],
                    'price': product[4],
                    'size': product[5],
                    'density': product[6],
                    'material': product[7],
                    'description': product[8],
                    'image': product[9],
                    'colors': colors
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting product: {e}")
            return None
        finally:
            conn.close()
    
    def add_to_cart(self, user_id, product_key, color=None):
        """Add product to cart"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Check if item already exists in cart
            cursor.execute("""
                SELECT id, quantity FROM cart 
                WHERE user_id = ? AND product_key = ? AND color = ?
            """, (user_id, product_key, color))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update quantity
                cursor.execute("""
                    UPDATE cart SET quantity = quantity + 1 
                    WHERE id = ?
                """, (existing[0],))
            else:
                # Add new item
                cursor.execute("""
                    INSERT INTO cart (user_id, product_key, color)
                    VALUES (?, ?, ?)
                """, (user_id, product_key, color))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error adding to cart: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_cart(self, user_id):
        """Get user's cart items"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.product_key, c.color, c.quantity, p.name, p.price
                FROM cart c
                JOIN products p ON c.product_key = p.product_key
                WHERE c.user_id = ?
                ORDER BY c.added_at
            """, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting cart: {e}")
            return []
        finally:
            conn.close()
    
    def create_order(self, user_id, product_key, color=None, quantity=1, delivery_address=None):
        """Create new order"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Get product price
            product = self.get_product(product_key)
            if not product:
                return None
            
            total_price = product['price'] * quantity
            
            cursor.execute("""
                INSERT INTO orders (user_id, product_key, color, quantity, total_price, delivery_address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, product_key, color, quantity, total_price, delivery_address))
            
            order_id = cursor.lastrowid
            conn.commit()
            
            return order_id
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_orders(self, user_id):
        """Get user's orders"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.product_key, o.color, o.quantity, o.total_price, 
                       o.status, o.payment_status, o.tracking_link, o.created_at, p.name, o.delivery_address
                FROM orders o
                JOIN products p ON o.product_key = p.product_key
                WHERE o.user_id = ?
                ORDER BY o.created_at DESC
            """, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting user orders: {e}")
            return []
        finally:
            conn.close()
    
    def clear_cart(self, user_id):
        """Remove all items from user's cart"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM cart WHERE user_id = ?",
                (user_id,)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
        finally:
            conn.close()
    
    def get_all_orders(self):
        """Get all orders for admin"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.user_id, o.product_key, o.color, o.quantity, o.total_price, 
                       o.status, o.payment_status, o.tracking_link, o.created_at, p.name, o.delivery_address
                FROM orders o
                JOIN products p ON o.product_key = p.product_key
                ORDER BY o.created_at DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting all orders: {e}")
            return []
        finally:
            conn.close()
    
    def get_order(self, order_id):
        """Get specific order"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.user_id, o.product_key, o.color, o.quantity, o.total_price, 
                       o.status, o.payment_status, o.tracking_link, o.created_at, p.name, o.delivery_address
                FROM orders o
                JOIN products p ON o.product_key = p.product_key
                WHERE o.id = ?
            """, (order_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error getting order: {e}")
            return None
        finally:
            conn.close()
    
    def update_order_status(self, order_id, status, payment_status=None):
        """Update order status"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            if payment_status:
                cursor.execute("""
                    UPDATE orders 
                    SET status = ?, payment_status = ? 
                    WHERE id = ?
                """, (status, payment_status, order_id))
            else:
                cursor.execute("""
                    UPDATE orders 
                    SET status = ? 
                    WHERE id = ?
                """, (status, order_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            return False
        finally:
            conn.close()