# 代码生成时间: 2025-09-29 18:28:45
import asyncio
from sanic import Sanic
from sanic.response import json, file
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load the pre-trained MobileNetV2 model
model = load_model('path_to_your_model.h5')

# Create the Sanic app
app = Sanic('ImageRecognitionService')

@app.route('/upload', methods=['POST'])
def upload_image(request):
    # Get the uploaded image from the request
    if 'image' not in request.files:
        return json({'error': 'No image provided'}, status=400)
    
    # Load the image from the request
    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.body))
    
    # Resize and preprocess the image for the model
    image = image.resize((224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    
    try:
        # Make a prediction using the model
        predictions = model.predict(image)
        
        # Assuming the model outputs class labels
        predicted_class = np.argmax(predictions)
        
        return json({'predicted_class': predicted_class}, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)
    
@app.route('/image', methods=['GET'])
def get_image(request):
    # Return a sample image
    return file('path_to_sample_image.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)