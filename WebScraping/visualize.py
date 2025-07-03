import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import logging

# Set Matplotlib backend to Agg for non-interactive environments
plt.switch_backend('Agg')

# Set up logging to console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('visualize_debug.log')
    ]
)
logger = logging.getLogger(__name__)

def clean_price(price):
    """Convert price string to float, handling ranges and currencies."""
    try:
        if not isinstance(price, str):
            logger.warning(f"Invalid price type: {type(price)} - {price}")
            return None
        price = price.replace('$', '').replace(',', '').strip()
        if '-' in price:
            price = price.split('-')[0].strip()
        return float(price)
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to clean price '{price}': {e}")
        return None

def clean_rating(rating):
    """Extract percentage from rating string."""
    try:
        if not isinstance(rating, str):
            return None
        # Handle formats like '98.7%' or 'sambasaturne (3) 100%'
        match = pd.Series([rating]).str.extract(r'(\d+\.\d+)%')[0].iloc[0]
        return float(match) if pd.notna(match) else None
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to clean rating '{rating}': {e}")
        return None

def visualize_data(excel_file='data/ebay_data.xlsx', output_dir='visualizations'):
    """Generate visualizations for price trends and rating distributions, stopping on failure."""
    logger.info(f"Starting visualization with excel_file: {excel_file}, output_dir: {output_dir}")
    
    # Check if Excel file exists
    if not os.path.exists(excel_file):
        logger.error(f"Excel file '{excel_file}' does not exist")
        raise FileNotFoundError(f"Excel file '{excel_file}' not found. Run run_scraper.py first.")
    
    # Create output directory
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
    except OSError as e:
        logger.error(f"Failed to create output directory '{output_dir}': {e}")
        raise OSError(f"Cannot create output directory: {e}")
    
    try:
        # Read Excel file
        logger.info(f"Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)
        if df.empty:
            logger.error("DataFrame is empty")
            raise ValueError("Excel file contains no data")
        logger.info(f"Loaded DataFrame with {len(df)} rows and columns: {list(df.columns)}")
        
        # Log sample data
        logger.info(f"Sample data (first 5 rows):\n{df.head().to_string()}")
        
        # Clean price data
        logger.info("Cleaning price data")
        df['price_numeric'] = df['price'].apply(clean_price)
        valid_prices = df['price_numeric'].notna().sum()
        logger.info(f"Valid price_numeric entries: {valid_prices}")
        if valid_prices == 0:
            logger.error("No valid price_numeric values after cleaning")
            raise ValueError("No valid prices available for plotting")
        df = df.dropna(subset=['price_numeric'])
        logger.info(f"After price cleaning, DataFrame has {len(df)} rows")
        
        # Plot 1: Average price by location
        logger.info("Generating average price by location plot")
        avg_price_by_location = df.groupby('location')['price_numeric'].mean().sort_values(ascending=False)[:10]
        if avg_price_by_location.empty:
            logger.error("No valid data for average price by location")
            raise ValueError("No valid location data for price plot")
        plt.figure(figsize=(12, 6))
        sns.barplot(x=avg_price_by_location.values, y=avg_price_by_location.index)
        plt.title('Average Price by Location (Top 10)')
        plt.xlabel('Average Price ($)')
        plt.ylabel('Location')
        price_plot_path = os.path.join(output_dir, 'price_trend.png')
        plt.savefig(price_plot_path, bbox_inches='tight')
        plt.close()
        if os.path.exists(price_plot_path):
            file_size = os.path.getsize(price_plot_path)
            logger.info(f"Successfully saved price trend plot to {price_plot_path} (size: {file_size} bytes)")
        else:
            logger.error(f"Failed to save price trend plot at {price_plot_path}")
            raise RuntimeError(f"Price trend plot not created at {price_plot_path}")
        
        # Clean rating data
        logger.info("Cleaning rating data")
        df['rating_numeric'] = df['rating'].apply(clean_rating)
        valid_ratings = df['rating_numeric'].notna().sum()
        logger.info(f"Valid rating_numeric entries: {valid_ratings}")
        
        # Plot 2: Rating distribution
        logger.info("Generating rating distribution plot")
        if valid_ratings < 10:  # Require at least 10 valid ratings
            logger.error(f"Insufficient valid ratings ({valid_ratings}) for histogram")
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'Insufficient valid ratings available', ha='center', va='center')
            plt.savefig(os.path.join(output_dir, 'rating_distribution.png'), bbox_inches='tight')
            plt.close()
            logger.info(f"Saved placeholder rating distribution plot to {output_dir}/rating_distribution.png")
        else:
            plt.figure(figsize=(10, 6))
            sns.histplot(df['rating_numeric'].dropna(), bins=20)
            plt.title('Distribution of Seller Ratings')
            plt.xlabel('Rating (%)')
            plt.ylabel('Count')
            rating_plot_path = os.path.join(output_dir, 'rating_distribution.png')
            plt.savefig(rating_plot_path, bbox_inches='tight')
            plt.close()
            if os.path.exists(rating_plot_path):
                file_size = os.path.getsize(rating_plot_path)
                logger.info(f"Successfully saved rating distribution plot to {rating_plot_path} (size: {file_size} bytes)")
            else:
                logger.error(f"Failed to save rating distribution plot at {rating_plot_path}")
                raise RuntimeError(f"Rating distribution plot not created at {rating_plot_path}")
        
        logger.info("Visualization completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Visualization failed: {e}", exc_info=True)
        raise
    
if __name__ == '__main__':
    try:
        success = visualize_data()
        if success:
            logger.info("Program completed successfully")
            sys.exit(0)
        else:
            logger.error("Program failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Program terminated due to error: {e}")
        sys.exit(1)