from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from PIL import Image
import io

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('New client connected')

@socketio.on('uploadImage')
def handle_upload_image(data):
    # Convert the uploaded image from base64 to bytes
    image_data = data.split(',')[1]
    image_bytes = io.BytesIO(base64.b64decode(image_data))

    # Open the image using PIL
    image = Image.open(image_bytes)

    # Convert the image to PNG format if it's in HEIC format
    if image.format == 'HEIC':
        image = image.convert('RGB')

    # Save the image as PNG
    output_bytes = io.BytesIO()
    image.save(output_bytes, format='PNG')
    output_bytes.seek(0)

    # Convert the PNG image back to base64
    png_base64 = base64.b64encode(output_bytes.read()).decode('utf-8')
    png_data = f'data:image/png;base64,{png_base64}'

    # Emit the converted image to all connected clients
    emit('newImage', png_data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, port=5000)