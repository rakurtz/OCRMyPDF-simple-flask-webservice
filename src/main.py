# OCR Webservice that uses Tesseract to extract text from pdfs
# subprocess: ocrmypdf -l deu --force-ocr --rotate-pages --rotate-pages-threshold 5

from flask import Flask, render_template, redirect, request, url_for, send_from_directory, session
import os
import subprocess
import uuid
import os

FLASK_PORT = os.environ['FLASK_PORT']
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

@app.route('/')
def index():
    error_message = request.args.get('error_message', "")
    return render_template('index.html', error_message=error_message)

@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    force_ocr = request.form.get('force_ocr', False)
    
    if file.filename.endswith('.pdf'):
        # Create the "uploads" directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('downloads', exist_ok=True)

        # Save the uploaded file with a uuid as the filename
        orig_file = f'{uuid.uuid4()}.pdf'
        orig_path = f'uploads/{orig_file}' # root is /app
        
        try:
            file.save(orig_path)
        except Exception as e:
            session['error_message'] = f'Error saving the file: {e}'
            return redirect(url_for('error'))
        
        # Create a unique filename for the processed PDF (only for the server side)
        target_file = f'{uuid.uuid4()}.pdf'
        target_path = f'downloads/{target_file}'
              
        session['filename'] = file.filename
        session['orig_filesize'] = os.path.getsize(orig_path)

        # Process the PDF using ocrmypdf
        try:
            if force_ocr:
                result = subprocess.run(['ocrmypdf', '-l', 'deu', '--force-ocr', '--deskew', '--rotate-pages', '--rotate-pages-threshold', '5', orig_path, target_path], capture_output=True, text=True)
            else:
                result = subprocess.run(['ocrmypdf', '-l', 'deu', '--rotate-pages', '--deskew', '--rotate-pages-threshold', '5', orig_path, target_path], capture_output=True, text=True) 
            
            
            # Return a link to download the processed PDF
            if result.returncode == 0 and os.path.exists(target_path):
                session['target_filesize'] = os.path.getsize(target_path)
                return redirect(url_for('results', link=target_file))
            else:
                session['error_message'] = f'OCR-Error processing the file: {result.stderr}'
                return redirect(url_for('error'))

        except subprocess.CalledProcessError as e:
            session['error_message'] = f'System-Error processing the file: {e}'
            return redirect(url_for('error'))
        
    else:
        return 'Invalid file format. Only PDF files are allowed.', 400

@app.route('/results/<link>')
def results(link):
        file_name = session.pop('filename', 'unknown filename')
        orig_filesize = f"{session.pop('orig_filesize', 0)/1024/1024:.2f}"  # get from session, default value 0, convert to MB
        target_filesize = f"{session.pop('target_filesize', 0)/1024/1024:.2f}"

        return render_template('results.html', download_url=url_for('download', link=link), orig_filesize=orig_filesize, target_filesize=target_filesize)

@app.route('/error')
def error():
        error_message = session.pop('error_message', 'Unknown error')
        file_name = session.pop('filename', 'unknown filename')
        return render_template('error.html', error_message=error_message, name=file_name )

@app.route('/download/<link>')
def download(link):
    file_name = session.pop('name', "file.pdf")
    return send_from_directory(
        '../downloads', link, as_attachment=True, download_name=f'ocr_{file_name}'
    )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=FLASK_PORT)