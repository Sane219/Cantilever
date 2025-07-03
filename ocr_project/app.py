from flask import Flask, render_template, request, redirect, url_for, send_file
from ocr_processor import extract_text
from database import store_ocr_result, get_all_ocr_results
import os
import sqlite3
import logging
import io

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render homepage with upload form and OCR results."""
    results = get_all_ocr_results()
    error = None
    success = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file uploaded'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'No file selected'
            elif not allowed_file(file.filename):
                error = 'Invalid file type. Use PNG, JPG, or JPEG'
            else:
                try:
                    filename = file.filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    result = extract_text(filepath)
                    store_ocr_result(result)
                    success = f"Successfully processed {filename}"
                    logger.info(f"Processed {filename}")
                except Exception as e:
                    error = f"Error processing file: {e}"
                    logger.error(error)
                return redirect(url_for('index'))
    
    return render_template('index.html', results=results, error=error, success=success)

@app.route('/clear', methods=['POST'])
def clear_database():
    """Clear all OCR results from the database."""
    try:
        conn = sqlite3.connect('data/ocr_data.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ocr_results')
        conn.commit()
        conn.close()
        logger.info("Database cleared")
        success = "Database cleared successfully"
    except sqlite3.Error as e:
        logger.error(f"Error clearing database: {e}")
        error = f"Error clearing database: {e}"
        return redirect(url_for('index'), error=error)
    return redirect(url_for('index'), success=success)

@app.route('/download/<path:image_path>')
def download_text(image_path):
    """Download extracted text as a .txt file."""
    try:
        conn = sqlite3.connect('data/ocr_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT text FROM ocr_results WHERE image_path = ?', (image_path,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] != 'N/A':
            text = result[0]
            return send_file(
                io.BytesIO(text.encode('utf-8')),
                mimetype='text/plain',
                as_attachment=True,
                download_name=f"{os.path.basename(image_path)}_text.txt"
            )
        error = "No text available for download"
        return redirect(url_for('index'), error=error)
    except Exception as e:
        logger.error(f"Error downloading text: {e}")
        error = f"Error downloading text: {e}"
        return redirect(url_for('index'), error=error)

if __name__ == '__main__':
    app.run(debug=True)