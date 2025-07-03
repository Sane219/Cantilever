import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db(db_name='data/ebay_data.db'):
    """Initialize SQLite database with a products table."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price TEXT,
                url TEXT,
                description TEXT,
                reviews TEXT,
                rating TEXT,
                location TEXT,
                units_sold TEXT
            )
        ''')
        conn.commit()
        logger.info("Database initialized")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None

def store_data(items, db_name='data/ebay_data.db'):
    """Store scraped items in SQLite database."""
    conn = init_db(db_name)
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        for item in items:
            cursor.execute('''
                INSERT INTO products (title, price, url, description, reviews, rating, location, units_sold)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['title'], item['price'], item['url'], item['description'],
                item['reviews'], item['rating'], item['location'], item['units_sold']
            ))
        conn.commit()
        logger.info(f"Stored {len(items)} items in database")
    except sqlite3.Error as e:
        logger.error(f"Error storing data: {e}")
    finally:
        conn.close()

def search_products(query, db_name='data/ebay_data.db'):
    """Search products by keyword in title or description."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT title, price, url, description, reviews, rating, location, units_sold
            FROM products
            WHERE title LIKE ? OR description LIKE ?
            LIMIT 100
        ''', (f'%{query}%', f'%{query}%'))
        results = [
            {
                'title': row[0], 'price': row[1], 'url': row[2], 'description': row[3],
                'reviews': row[4], 'rating': row[5], 'location': row[6], 'units_sold': row[7]
            }
            for row in cursor.fetchall()
        ]
        logger.info(f"Found {len(results)} results for search query: {query}")
        return results
    except sqlite3.Error as e:
        logger.error(f"Search error: {e}")
        return []
    finally:
        conn.close()