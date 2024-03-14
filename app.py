# Flask app
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

# File management
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# QR code generation (through base64 and cookie handling)
import os
import qrcode
from io import BytesIO
import base64


app = Flask(__name__)
app.secret_key = 'very_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# Function to delete old files (right not it is every 5 minutes for every file older than 5 minutes)
def cleanup_old_files():
    now = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            stat = os.stat(path)
            creation_time = datetime.fromtimestamp(stat.st_ctime)
            if now - creation_time > timedelta(minutes=5):  # Deletes files older than 5 minutes
                os.remove(path)
                print(f"Deleted {path}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_old_files, trigger="interval", minutes=1)  # Runs every 5 minutes
scheduler.start()

# Important!!!!!!!
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = os.urandom(24).hex()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Generate QR code with the URL to upload files
    request_url = f'{request.url_root}upload?session_id={session["user_id"]}'

    qr.add_data(request_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Make it a base64 string
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Retrieve list of uploaded file URLs for the session so that it syncs when uploaded in the same
    # session
    uploaded_files_urls = session.get('uploaded_files_urls', [])

    # Return the qr str, list of urls, and qr code url (temp since we haven't deployed yet)
    return render_template('index.html', qr_code_data=img_str, uploaded_files_urls=uploaded_files_urls, qr_code_url=request_url)

# This route is used to upload files to the server
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    session_id = request.args.get('session_id', '')

    # Check if the session ID is valid
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename != '':
            # Save the file to the server
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{session_id}_{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Append the new file URL to the list in the session
            if 'uploaded_files_urls' not in session:
                session['uploaded_files_urls'] = []
            session['uploaded_files_urls'].append(url_for('static', filename=f'images/{filename}'))
            session.modified = True  # Ensure the session is marked as modified

    # Return the upload page
    return render_template('upload.html')

@app.route('/reset')
def reset_session():
    # This is hooked up with a button on the front end to reset the session (a.k.a clean images uploaded)
    session.pop('user_id', None)  # Remove the current session ID
    session.pop('uploaded_files_urls', None)  # Clear the list of uploaded files
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
