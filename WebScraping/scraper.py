import requests
from bs4 import BeautifulSoup
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_session_with_retries():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def scrape_ebay_items(query, max_entries=10000, items_per_page=100):
    """
    Scrape eBay search results for items.
    Args:
        query (str): Search keyword (e.g., 'laptop')
        max_entries (int): Maximum number of entries to scrape
        items_per_page (int): Items per page (max 100)
    Returns:
        list: List of dictionaries with item details
    """
    base_url = 'https://www.ebay.com/sch/i.html'
    session = create_session_with_retries()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    results = []
    page = 1
    items_collected = 0
    
    while items_collected < max_entries:
        params = {
            '_nkw': query,
            '_sacat': 0,
            '_ipg': items_per_page,
            '_pgn': page
        }
        
        try:
            logger.info(f"Fetching page {page} for query: {query}")
            time.sleep(3)  # Delay to avoid rate limiting
            response = session.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Successfully fetched page {page}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='s-item__wrapper')
            if not items:
                logger.warning(f"No items found on page {page}. Stopping.")
                break
            
            for item in items:
                if items_collected >= max_entries:
                    break
                
                # Extract title
                title_tag = item.find('div', class_='s-item__title')
                title = title_tag.text.strip() if title_tag else 'N/A'
                
                # Extract price
                price_tag = item.find('span', class_='s-item__price')
                price = price_tag.text.strip() if price_tag else 'N/A'
                
                # Extract URL
                url_tag = item.find('a', class_='s-item__link')
                url = url_tag['href'] if url_tag else 'N/A'
                
                # Extract description (limited in search results, may need item page)
                desc_tag = item.find('div', class_='s-item__subtitle')
                description = desc_tag.text.strip() if desc_tag else 'N/A'
                
                # Extract reviews
                reviews_tag = item.find('span', class_='s-item__reviews-count')
                reviews = reviews_tag.text.strip().split()[0] if reviews_tag else 'N/A'
                
                # Extract star rating
                rating_tag = item.find('span', class_='s-item__seller-info-text')
                rating = rating_tag.text.strip() if rating_tag else 'N/A'
                
                # Extract location
                location_tag = item.find('span', class_='s-item__location')
                location = location_tag.text.strip().replace('from ', '') if location_tag else 'N/A'
                
                # Extract units sold
                sold_tag = item.find('span', class_='s-item__quantity-sold')
                units_sold = sold_tag.text.strip().split()[0] if sold_tag else 'N/A'
                
                results.append({
                    'title': title,
                    'price': price,
                    'url': url,
                    'description': description,
                    'reviews': reviews,
                    'rating': rating,
                    'location': location,
                    'units_sold': units_sold
                })
                
                items_collected += 1
            
            logger.info(f"Collected {items_collected} items so far")
            page += 1
            
            next_page = soup.find('a', class_='pagination__next')
            if not next_page or 'disabled' in next_page.get('class', []):
                logger.info("No more pages available.")
                break
            
        except requests.RequestException as e:
            logger.error(f"Error fetching page {page}: {e}")
            if "Temporary failure in name resolution" in str(e):
                logger.warning("DNS resolution error. Retrying after 10 seconds...")
                time.sleep(10)
                continue
            break
    
    return results