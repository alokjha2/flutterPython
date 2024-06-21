import sys
sys.path.append('lipsproject/backend/')  # Add the backend folder to the system path

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import io

from run import evaluate  # Import evaluate from backend folder

app = Flask(__name__)
CORS(app)

@app.route('/eye-color-changer', methods=['POST'])
def process_image():
    # Check if the request contains an 'image' file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Read the image file from the request
    image_file = request.files['image']

    # Save the image to a temporary file
    image_path = 'temp_image.jpg'
    image_file.save(image_path)

    # Process the image using the evaluate function
    evaluate(input_path=image_path, output_path='output.jpg', mode='red')

    # Read the processed image
    with open('output.jpg', 'rb') as f:
        processed_image = f.read()

    # Return the processed image
    response = make_response(processed_image)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

# debug 
# if __name__ == '__main__':
#     app.run(host='192.168.3.240', port=5000, debug=True) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
