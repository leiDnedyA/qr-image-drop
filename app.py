# Flask app
from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit, join_room

import re

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

# Generate IDs for sessions
import uuid

app = Flask(__name__)
app.secret_key = 'very_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

socketio = SocketIO(app)

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

# Function to delete old files (right not it is every 5 minutes for every file older than 5 minutes)
def cleanup_old_files():
    now = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Make sure not to delete .gitignore so that upload folder is tracked
        if path.endswith('.gitignore'):
            continue
        if os.path.isfile(path):
            stat = os.stat(path)
            creation_time = datetime.fromtimestamp(stat.st_ctime)
            if now - creation_time > timedelta(minutes=5):  # Deletes files older than 5 minutes
                os.remove(path)
                print(f"Deleted {path}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_old_files, trigger="interval", minutes=5)  # Runs every 5 minutes
scheduler.start()

# Important!!!!!!!
atexit.register(lambda: scheduler.shutdown())

# Key: UUID, value: [list of image ids for session]
sessions = {}

@app.route('/')
def index():

    user_agent = request.headers.get('User-Agent', '')

    device_type_match = re.search(r'\(([^;)]+)', user_agent)

    device_type = device_type_match.group(1) if device_type_match else ''

    is_mobile = device_type.lower() in ['iphone', 'android']

    print(f"User agent: {device_type}")

    user_id_cookie = request.cookies.get('user_id')
    if not user_id_cookie or not user_id_cookie in sessions:
        # Set up session
        user_id = str(uuid.uuid4())
        sessions[user_id] = []
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

    # Retrieve list of uploaded file URLs for the session so that it syncs when uploaded in the same
    # session
    uploaded_files_urls = sessions[user_id]

    # Return the qr str, list of urls, and qr code url (temp since we haven't deployed yet)
    rendered_template = render_template('index.html', is_mobile=is_mobile, qr_code_data=img_str, uploaded_files_urls=uploaded_files_urls, qr_code_url=request_url, session=user_id)
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
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{session_id}_{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Check if the uploaded file is HEIC format; if so, convert to JPG
            if filename.lower().endswith('.heic'):
                file_path = convert_heic_to_png(file_path)
                # Update filename to the new png filename
                filename = filename.rsplit('.', 1)[0] + '.png'
                print(f"Converted HEIC to PNG: {filename}")

            # Append the new file URL to the list in the session
            if session_id in sessions:
#                sessions[session_id].append(url_for('static', filename=f'images/{filename}'))
                sessions[session_id].append(f'{GLOBAL_URL_ROOT}static/images/{filename}')


            # Increment the counter value
            counter_file = 'static/counter.txt'
            with open(counter_file, 'r') as f:
                count = int(f.read())
            with open(counter_file, 'w') as f:
                f.write(str(count + 1))

        # Return the upload page
    return render_template('upload.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    print(f'Client joined room: {room}')

@socketio.on('share_qr')
def handle_share_qr(data):
    qr_code_url = data['qr_code_url']
    print(f'Received share_qr event')
    emit('qr_code_shared', {'qr_code_url': qr_code_url}, broadcast=True, skip_sid=request.sid)

@app.route('/session_links', methods=['GET'])
def get_session_links():
    session_id = request.args.get('session_id')

    if not session_id:
        return make_response('Missing query param "session_id"', 400)
    if not session_id in sessions:
        return make_response('Session not found with provided ID', 404)

    return jsonify(sessions[session_id])
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
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user_id', '', expires=0)
    return response

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
