import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db(db_name='data/ocr_data.db'):
    """Initialize SQLite database with an ocr_results table."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocr_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT,
                text TEXT,
                error TEXT
            )
        ''')
        conn.commit()
        logger.info("Database initialized")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None

def store_ocr_result(result, db_name='data/ocr_data.db'):
    """Store OCR result in SQLite database."""
    conn = init_db(db_name)
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ocr_results (image_path, text, error)
            VALUES (?, ?, ?)
        ''', (result['image_path'], result['text'], result['error']))
        conn.commit()
        logger.info(f"Stored OCR result for {result['image_path']}")
    except sqlite3.Error as e:
        logger.error(f"Error storing OCR result: {e}")
    finally:
        conn.close()

def get_all_ocr_results(db_name='data/ocr_data.db'):
    """Retrieve all OCR results from the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT image_path, text, error FROM ocr_results')
        results = [{'image_path': row[0], 'text': row[1], 'error': row[2]} for row in cursor.fetchall()]
        logger.info(f"Retrieved {len(results)} OCR results")
        return results
    except sqlite3.Error as e:
        logger.error(f"Error retrieving OCR results: {e}")
        return []
    finally:
        conn.close()