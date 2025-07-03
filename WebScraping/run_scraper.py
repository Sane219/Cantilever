from scraper import scrape_ebay_items
from database import store_data
import pandas as pd
import os
     
def main():
         # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
         
         # Scrape 10,000 entries
    items = scrape_ebay_items('laptop', max_entries=10000, items_per_page=100)
         
    if items:
             # Store in SQLite
        store_data(items, db_name='data/ebay_data.db')
             # Store in Excel
        pd.DataFrame(items).to_excel('data/ebay_data.xlsx', index=False)
        print(f"Scraped and stored {len(items)} items")
    else:
        print("No items scraped")
     
if __name__ == '__main__':
    main()