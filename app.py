# Flask app
from typing import Dict
from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
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

# Heic handle
from Utils.handleHeic import convert_heic_to_png
from Utils.session import Session
from threading import Thread

# Generate IDs and timestamps for sessions
import uuid

# Security
from flask_talisman import Talisman
from Config.security import talisman_settings
import secrets

ACCEPTED_FILETYPES = set(["png", "jpg", "jpeg", "heic", "webp", "svg", "gif", "pdf"])

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# Set secure headers and best practices
csp = {
    'default-src': ["'self'", 'fonts.googleapis.com', '*.google-analytics.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com'],
    'img-src': ['*', 'data:', 'blob:', '*.google-analytics.com', '*.googletagmanager.com', '*.buymeacoffee.com'],
    'script-src': ["'self'", "'unsafe-inline'", '*.google-analytics.com', '*.googletagmanager.com', '*.buymeacoffee.com'],
    'style-src': ["'self'", "'unsafe-inline'", 'fonts.googleapis.com', 'cdnjs.cloudflare.com'],
    'frame-src': ['www.buymeacoffee.com', 'buymeacoffee.com', "'self'"]
}

talisman = Talisman(app)

for key, value in talisman_settings.items():
    setattr(talisman, key, value)

talisman.content_security_policy = csp

def get_url_root(request):
    """
    Returns the URL root to use for generating qr codes, given a Flask request object.

    Useful in case we are using a reverse-proxy with a different location and want
    the upload page to contain the same location.
    """
    if "X-Full-Request-URL" in request.headers:
        url_root = request.headers["X-Full-Request-URL"]
    else:
        url_root = request.url_root
    return url_root

# Used to store the URL for the home route to account for reverse proxies
GLOBAL_URL_ROOT = None

# Key: UUID, value: `Session` instance
sessions: Dict[str, Session] = {}

# Function to delete old files and sessions (right not it is every 5 minutes for every file older than 5 minutes)
def cleanup_old_files():
    now = datetime.now()
    sessions_to_delete = []
    for session_id in sessions:
        session = sessions[session_id]
        if now - session.timestamp > timedelta(minutes=5):
            for image_url in session.images:
                split_image_url = image_url.split("/")
                if len(split_image_url) == 0:
                    app.logger.warning(f"warning: corrupted session data for session {session_id}")
                    continue
                image_filename = split_image_url[-1]
                image_path = f'{app.config["UPLOAD_FOLDER"]}/{image_filename}'
                if os.path.exists(image_path):
                    os.remove(image_path)
            app.logger.info(f"deleting session with ID {session_id}")
            sessions_to_delete.append(session_id)
    for session_id in sessions_to_delete:
        del sessions[session_id]
    # Check to see if any files not associated with a session exist from over 5 minutes ago
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Make sure not to delete .gitignore so that upload folder is tracked
        if path.endswith('.gitkeep'):
            continue
        if os.path.isfile(path):
            stat = os.stat(path)
            creation_time = datetime.fromtimestamp(stat.st_ctime)
            if now - creation_time > timedelta(minutes=5):  # Deletes files older than 5 minutes
                os.remove(path)
                app.logger.info(f"Deleted {path}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_old_files, trigger="interval", minutes=5)  # Runs every 5 minutes
scheduler.start()

# Important!!!!!!!
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    user_id_cookie = request.cookies.get('user_id')
    if not user_id_cookie or not user_id_cookie in sessions:
        # Set up session
        user_id = str(uuid.uuid4())
        sessions[user_id] = Session(user_id)
    else:
        user_id = user_id_cookie

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )


    # Update the URL root based on requests made to "/"
    url_root = get_url_root(request)
    global GLOBAL_URL_ROOT
    GLOBAL_URL_ROOT = url_root

    # Generate QR code with the URL to upload files
    request_url = f'{url_root}upload?session_id={user_id}'

    # request_url = f'{request.url_root}upload?session_id=test' # use this to test invalid session handling

    qr.add_data(request_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000", back_color="#eda400")
    
    # Make it a base64 string
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Return the qr str, list of urls, and qr code url (temp since we haven't deployed yet)
    rendered_template = render_template('index.html', qr_code_data=img_str, qr_code_url=request_url, session=user_id)
    response = make_response(rendered_template)
    if not request.cookies.get('user_id') or request.cookies.get('user_id') != user_id:
        response.set_cookie('user_id', user_id)
    return response



# This route is used to upload files to the server
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    session_id = request.args.get('session_id', '')

    if not session_id in sessions:
        return make_response('<h1>Invalid session, press "Reset Session" button on the main page and try again</h1>')

    # Check if the session ID is valid
    if request.method == 'POST':
        file = request.files.get('file')
        if file.filename == '':
            return render_template('upload.html',error='Please upload a file')
        if file and file.filename != '':
            # Save the file to the server

            if not '.' in file.filename:
                return render_template('upload.html', error=f'Error: The file "{file.filename}" is not an accepted file type. Nice try buddy ;)')

            file_extension = file.filename.split('.')[-1]

            if not file_extension.lower() in ACCEPTED_FILETYPES:
                return render_template('upload.html', error=f'Error: {file_extension} extension is not supported.')

            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{session_id}_{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Check if the uploaded file is HEIC format; if so, convert to PNG
            if filename.lower().endswith('.heic'):
                # Use separate thread for conversion to keep response time for /upload endpoint low
                def task(file_path, filename, sessions):
                    file_path = convert_heic_to_png(file_path)
                    filename = filename.rsplit('.', 1)[0] + '.png' # filename.heic -> filename.png
                    app.logger.info(f"Converted HEIC to PNG: {filename}")
                    if session_id in sessions:
                        sessions[session_id].add_image(f'{GLOBAL_URL_ROOT}static/images/{filename}')
                        sessions[session_id].loading_count -= 1
                thread = Thread(target=task, args=(file_path, filename, sessions))
                sessions[session_id].loading_count += 1
                thread.start()
            else:
                # Otherwise, don't convert
                if session_id in sessions:
                    sessions[session_id].add_image(f'{GLOBAL_URL_ROOT}static/images/{filename}')


            # Increment the counter value
            counter_file = 'static/counter.txt'
            with open(counter_file, 'r') as f:
                count = int(f.read())
            with open(counter_file, 'w') as f:
                f.write(str(count + 1))

        # Return the upload page
    return render_template('upload.html')

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.route('/session_links', methods=['GET'])
def get_session_links():
    session_id = request.args.get('session_id')

    if not session_id:
        return make_response('Missing query param "session_id"', 400)
    if not session_id in sessions:
        return make_response('Session not found with provided ID', 404)

    return jsonify({
        "images": sessions[session_id].images,
        "loading_count": sessions[session_id].loading_count
        })
    return ":)"

@app.route('/counter')
def get_counter():
    counter_file = 'static/counter.txt'
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as f:
            f.write('0')
    with open(counter_file, 'r') as f:
        count = f.read()
    return count


@app.route('/reset')
def reset_session():
    # This is hooked up with a button on the front end to reset the session (a.k.a clean images uploaded)
    # session.pop('user_id', None)  # Remove the current session ID
    # session.pop('uploaded_files_urls', None)  # Clear the list of uploaded files
    user_id_cookie = request.cookies.get('user_id')
    if user_id_cookie in sessions:
        del sessions[user_id_cookie]
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user_id', '', expires=0)
    return response

# Health Check endpoint
@app.route('/vet')
def vet():
    return 'ok 🕊️'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
