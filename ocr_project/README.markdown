# OCR Text Extraction Project

This project implements an Optical Character Recognition (OCR) web application that extracts text from images using Tesseract OCR. It includes a Flask-based web interface for uploading images, displaying extracted text, downloading results, and clearing the database. The application automatically downloads a dataset of scanned images from Kaggle for testing and stores results in a SQLite database. The UI is styled with Tailwind CSS for a modern, professional look.

## Features
- **Automatic Dataset Download**: Downloads the [Scanned Images Dataset for OCR and VLM Finetuning](https://www.kaggle.com/datasets/suvroo/scanned-images-dataset-for-ocr-and-vlm-finetuning) using the Kaggle API.
- **OCR Processing**: Uses Tesseract OCR to extract text from images with preprocessing (grayscale, thresholding) for improved accuracy.
- **Web Interface**: Flask app with a responsive UI featuring:
  - Image upload (PNG/JPG/JPEG).
  - Card-based display of extracted text and image previews.
  - Download extracted text as `.txt` files.
  - Option to clear the database.
- **Database Storage**: Stores OCR results (image path, text, errors) in SQLite (`data/ocr_data.db`).
- **Error Handling**: Robust logging for Kaggle API, OCR, and database operations.
- **Modern UI**: Tailwind CSS for a professional, responsive design with a header, footer, and loading indicator.

## Project Structure
```
ocr_project/
├── ocr_processor.py        # Tesseract OCR processing
├── database.py            # SQLite database operations
├── app.py                 # Flask web application
├── process_images.py      # Downloads Kaggle dataset and processes images
├── templates/
│   └── index.html         # HTML template with Tailwind CSS
├── static/
│   ├── uploads/           # Uploaded images
│   ├── favicon.ico        # Favicon for browser icon
│   └── images/            # Kaggle dataset images
├── data/
│   └── ocr_data.db        # SQLite database
├── README.md              # This file
```

## Requirements
### Software
- **Python 3.8+**: Download from https://www.python.org/downloads/.
- **Tesseract OCR**: Install and add to PATH.
  - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki and add `C:\Program Files\Tesseract-OCR\tesseract.exe` to PATH.
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`
  - Verify: `tesseract --version`
- **VS Code (Recommended)**: For running and debugging. Download from https://code.visualstudio.com/.

### Python Dependencies
Install via pip:
```bash
pip install flask pillow pytesseract opencv-python sqlite3 kaggle
```

### Kaggle API
- Install: `pip install kaggle`
- Set up API token:
  - Go to Kaggle > Account > Create New API Token to download `kaggle.json`.
  - Place in:
    - Windows: `C:\Users\<YourUsername>\.kaggle\`
    - macOS/Linux: `~/.kaggle/`
  - Set permissions (macOS/Linux): `chmod 600 ~/.kaggle/kaggle.json`
- Verify: `kaggle datasets list`

### Dataset
- **Source**: [Scanned Images Dataset for OCR and VLM Finetuning](https://www.kaggle.com/datasets/suvroo/scanned-images-dataset-for-ocr-and-vlm-finetuning)
- Automatically downloaded by `process_images.py` to `static/images/`.
- Contains scanned document images suitable for OCR.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd ocr_project
   ```

2. **Create Folders**:
   ```bash
   mkdir static/uploads static/images data
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask pillow pytesseract opencv-python sqlite3 kaggle
   ```

4. **Set Up Favicon** (Optional, to avoid 404 error):
   - Download a 32x32 ICO file from https://www.favicon.io/ (e.g., a "T" icon).
   - Place in `static/favicon.ico`.
   - Alternatively, ignore the cosmetic `favicon.ico` 404 error.

5. **Configure Kaggle API**:
   - Place `kaggle.json` in the appropriate directory (see Requirements).
   - Ensure internet connectivity for dataset download.

## Usage
1. **Process Dataset**:
   - Run `process_images.py` to download the Kaggle dataset and extract text from up to 10 images:
     ```bash
     python process_images.py
     ```
   - **Output**: Populates `data/ocr_data.db` with OCR results and places images in `static/images/`.
   - **Note**: Adjust `max_images` in `process_images.py` to process more images.

2. **Run Flask App**:
   - Run `app.py`:
     ```bash
     python app.py
     ```
   - Open `http://127.0.0.1:5000` in a browser.
   - **Features**:
     - Upload images (PNG/JPG/JPEG) to extract text.
     - View results in a card layout with image previews and download links.
     - Clear the database using the "Clear Database" button.

3. **Debugging in VS Code**:
   - Open project in VS Code (`File > Open Folder`).
   - Set Python interpreter: `Ctrl+Shift+P`, `Python: Select Interpreter`.
   - Run scripts: Click the "Run" button or use terminal commands.
   - Check logs in the terminal for errors (e.g., "Processed image1.jpg").
   - Set breakpoints in `app.py` or `process_images.py` for debugging.

## Troubleshooting
- **Kaggle API Errors**:
  - Ensure `kaggle.json` is in the correct directory with proper permissions.
  - Verify internet connectivity and Kaggle account access.
  - Test API: `kaggle datasets list`.
- **Database Error (`no such table: ocr_results`)**:
  - Run `process_images.py` or upload an image via the Flask app to initialize `data/ocr_data.db`.
  - Verify: `sqlite3 data/ocr_data.db "SELECT * FROM ocr_results LIMIT 5;"`
- **OCR Issues**:
  - Ensure Tesseract is in PATH (`tesseract --version`).
  - If text extraction is inaccurate, check image quality or adjust preprocessing in `ocr_processor.py` (e.g., `cv2.threshold(gray, 100, 255, ...)`).
- **Favicon 404**: Ensure `static/favicon.ico` exists or ignore the error (cosmetic).

## Legal Notes
- **Dataset**: Used under Kaggle’s terms of service. Ensure compliance when redistributing.
- **Tesseract OCR**: Open-source under Apache 2.0 License.

## Submission
- **GitHub Repository**:
  - Initialize: `git init`
  - Add files, excluding `kaggle.json`:
    ```bash
    echo "kaggle.json" >> .gitignore
    git add .
    git commit -m "Complete OCR project with Kaggle dataset"
    git remote add origin <your-repo-url>
    git push -u origin main
    ```
  - Include a sample `data/ocr_data.db` (from 5–10 images).
- Submit the repository link via the internship form.

## Enhancements
- Add text search functionality to filter OCR results.
- Support multiple languages in Tesseract (`--lang eng+fra`).
- Enhance preprocessing for handwritten or low-quality images.

For issues or questions, contact the repository maintainer or check logs in VS Code’s terminal.
