from flask import Flask, render_template, request
from database import search_products
import pandas as pd
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render homepage with product data and search functionality."""
    query = request.form.get('search', '')
    products = []
    error = None
    
    try:
        if query:
            products = search_products(query)
        else:
            # Load a sample of data (first 100 rows)
            conn = sqlite3.connect('data/ebay_data.db')
            products = pd.read_sql_query("SELECT * FROM products LIMIT 100", conn).to_dict('records')
            conn.close()
        
    except sqlite3.OperationalError as e:
        error = f"Database error: {e}. Ensure 'data/ebay_data.db' exists and is populated."
        logger.error(error)
    except Exception as e:
        error = f"Unexpected error: {e}"
        logger.error(error)
    
    return render_template('index.html', products=products, query=query, error=error)

if __name__ == '__main__':
    app.run(debug=True)