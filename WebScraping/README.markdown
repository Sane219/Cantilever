# eCommerce Web Scraper

This project is a web scraping application for extracting product data from eBay, storing it in SQLite and Excel, visualizing trends, and providing a web interface with search functionality. It fulfills the requirements of the "01 Webscraping (ecommerce)" internship task, scraping up to 10,000 entries with fields like title, price, description, reviews, rating, location, and units sold.

## Features
- **Web Scraping**: Scrapes product data (title, price, URL, description, reviews, rating, location, units sold) from eBay using `requests` and `BeautifulSoup`.
- **Data Storage**: Stores data in a SQLite database (`data/ebay_data.db`) and Excel file (`data/ebay_data.xlsx`).
- **Visualization**: Generates plots for price trends (average price by location) and rating distributions using Matplotlib and Seaborn, saved in `visualizations/`.
- **Search Functionality**: Allows users to search products by keyword in title or description via a Flask web interface.
- **Web Interface**: Displays scraped data in a table with a search bar using Flask.

## Project Structure
```
ecommerce_scraper/
├── scraper.py              # Scraping logic for eBay
├── database.py            # SQLite database operations (store, search)
├── visualize.py           # Visualization logic for price and rating trends
├── app.py                 # Flask app for UI and search
├── run_scraper.py         # Orchestrates scraping and storage
├── templates/
│   └── index.html         # HTML template for Flask UI
├── static/
│   └── style.css          # CSS for UI styling
├── data/
│   ├── ebay_data.xlsx     # Excel output of scraped data
│   └── ebay_data.db       # SQLite database
├── visualizations/
│   ├── price_trend.png    # Average price by location
│   └── rating_distribution.png  # Rating distribution
├── README.md              # This file
```

## Prerequisites
- **Python 3.8+**: Install from https://www.python.org/downloads/.
- **VS Code**: Recommended IDE, download from https://code.visualstudio.com/.
- **Dependencies**: Install required Python libraries:
  ```bash
  pip install requests beautifulsoup4 pandas openpyxl matplotlib seaborn flask urllib3
  ```
- **Optional**: ChromeDriver for Selenium (if switching to Selenium for scraping).

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd ecommerce_scraper
   ```

2. **Set Up Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   ```
   - Activate:
     - Windows: `venv\Scripts\activate`
     - macOS/Linux: `source venv/bin/activate`

3. **Install Dependencies**:
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl matplotlib seaborn flask urllib3
   ```

4. **Open in VS Code**:
   - Launch VS Code and open the `ecommerce_scraper` folder (`File > Open Folder`).
   - Select the Python interpreter (`Ctrl+Shift+P`, then `Python: Select Interpreter`) and choose the virtual environment (`venv/bin/python` or `venv\Scripts\python.exe`).

5. **Ensure Folder Structure**:
   - Create `data/` and `visualizations/` folders if missing.
   - Verify `templates/index.html` and `static/style.css` are in place.

## Usage
1. **Scrape and Store Data**:
   - Run `run_scraper.py` to scrape 10,000 eBay entries for the query "laptop" (modify query in `run_scraper.py` if needed):
     ```bash
     python run_scraper.py
     ```
   - **Output**: Creates `data/ebay_data.xlsx` (Excel) and `data/ebay_data.db` (SQLite).
   - **Time**: ~1–2 hours due to delays to avoid rate limiting.
   - **Note**: If DNS errors occur, see Troubleshooting.

2. **Generate Visualizations**:
   - Run `visualize.py` to create plots:
     ```bash
     python visualize.py
     ```
   - **Output**: Saves `price_trend.png` (average price by location) and `rating_distribution.png` (rating distribution) in `visualizations/`.

3. **Run Flask App**:
   - Run `app.py` to start the web interface:
     ```bash
     python app.py
     ```
   - Open `http://127.0.0.1:5000` in a browser.
   - **Features**:
     - Displays up to 100 products in a table.
     - Search bar filters products by title or description.
   - **Note**: Ensure `data/ebay_data.db` exists before running.

## Running in