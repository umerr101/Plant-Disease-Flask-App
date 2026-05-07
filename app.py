"""
Flask Web Application for Plant Disease Classification
"""

import os
import pickle
import numpy as np
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import joblib

from utils import extract_image_features

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model and class names
MODEL_PATH = './models/plant_disease_model.joblib'
CLASS_NAMES_PATH = './models/class_names.pkl'

try:
    model_bundle = joblib.load(MODEL_PATH)
    model = model_bundle['pipeline']
    with open(CLASS_NAMES_PATH, 'rb') as f:
        class_names = pickle.load(f)
    model_loaded = True
    print("Model loaded successfully!")
except Exception as e:
    model_loaded = False
    print(f"Error loading model: {e}")
    print("Please train the model first by running: python train_model.py")

IMG_SIZE = 128


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        img = Image.open(image_path).convert('RGB')
        feature_vector = extract_image_features(image_path)
        img = img.resize((128, 128))
        return feature_vector.reshape(1, -1), img
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""

    if not model_loaded:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first.'
        }), 500

    # Check if file is present
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess image
        img_array, original_img = preprocess_image(filepath)

        # Make prediction
        predictions = model.predict_proba(img_array)
        confidence = float(np.max(predictions))
        predicted_class_idx = int(np.argmax(predictions))
        predicted_class = class_names[predicted_class_idx]

        # Get all predictions sorted by confidence
        all_predictions = []
        for idx, class_name in enumerate(class_names):
            all_predictions.append({
                'class': class_name,
                'confidence': float(predictions[0][idx])
            })
        all_predictions.sort(key=lambda x: x['confidence'], reverse=True)

        # Provide disease information
        disease_info = get_disease_info(predicted_class)

        return jsonify({
            'success': True,
            'predicted_disease': predicted_class,
            'confidence': confidence,
            'confidence_percentage': f"{confidence * 100:.2f}%",
            'all_predictions': all_predictions[:5],  # Top 5 predictions
            'disease_info': disease_info,
            'upload_filename': filename
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'num_classes': len(class_names) if model_loaded else 0,
        'classes': class_names if model_loaded else []
    })


def get_disease_info(disease_name):
    """Get information about a plant disease"""

    disease_database = {
        'Tomato_healthy': {
            'name': 'Healthy Tomato',
            'description': 'The plant appears to be healthy with no visible signs of disease.',
            'symptoms': 'No symptoms - plant is thriving',
            'treatment': 'Continue regular care and maintenance',
            'prevention': 'Maintain proper watering, sunlight, and soil conditions'
        },
        'Tomato_Early_blight': {
            'name': 'Early Blight',
            'description': 'Early blight is a fungal disease caused by Alternaria tomatophila.',
            'symptoms': 'Brown spots with concentric rings on lower leaves, often forming a target-like pattern',
            'treatment': 'Remove infected leaves, apply fungicide (chlorothalonil, mancozeb), ensure good air circulation',
            'prevention': 'Avoid overhead watering, mulch to prevent soil splash, remove debris, crop rotation'
        },
        'Tomato_Late_blight': {
            'name': 'Late Blight',
            'description': 'Caused by the pathogen Phytophthora infestans, this is a serious disease.',
            'symptoms': 'Water-soaked spots with white mold on leaf undersides, rapid spread',
            'treatment': 'Apply copper-based fungicides or systemics like chlorothalonil, remove infected parts',
            'prevention': 'Plant resistant varieties, avoid overhead watering, ensure good drainage and air flow'
        },
        'Tomato_Leaf_Mold': {
            'name': 'Leaf Mold',
            'description': 'Caused by Passalora fulva, spreads in warm, humid conditions.',
            'symptoms': 'Yellow patches on upper leaves, gray-brown powder on undersides',
            'treatment': 'Reduce humidity, improve ventilation, apply sulfur or copper fungicides',
            'prevention': 'Maintain low humidity, space plants well, remove infected leaves promptly'
        },
        'Tomato_Septoria_leaf_spot': {
            'name': 'Septoria Leaf Spot',
            'description': 'Caused by the fungus Septoria lycopersici.',
            'symptoms': 'Small circular spots with dark margins and gray centers with dark specks',
            'treatment': 'Remove infected leaves, apply fungicides (chlorothalonil), improve air circulation',
            'prevention': 'Avoid overhead watering, remove debris, practice crop rotation'
        },
        'Tomato_Spider_mites_Two_spotted_spider_mite': {
            'name': 'Spider Mites',
            'description': 'Tiny pests that cause damage by feeding on plant cells.',
            'symptoms': 'Fine webbing, yellowing leaves, speckled appearance, leaf drop',
            'treatment': 'Spray with neem oil, insecticidal soap, increase humidity, use miticides if severe',
            'prevention': 'Regular inspection, avoid stress to plants, maintain proper humidity'
        },
        'Tomato__Target_Spot': {
            'name': 'Target Spot',
            'description': 'Caused by Corynespora cassiicola fungus.',
            'symptoms': 'Circular spots with concentric rings resembling a target on leaves and fruits',
            'treatment': 'Apply copper-based fungicides, remove infected material, improve air circulation',
            'prevention': 'Use resistant varieties, avoid overhead watering, remove plant debris'
        },
        'Tomato__Tomato_mosaic_virus': {
            'name': 'Tomato Mosaic Virus',
            'description': 'Viral disease spread by contact and insects.',
            'symptoms': 'Mosaic pattern on leaves, mottling, leaf curl, stunted growth',
            'treatment': 'Remove infected plants, disinfect tools, no chemical cure available',
            'prevention': 'Use virus-free seeds, control aphids, avoid handling wet plants, sanitize tools'
        },
        'Tomato__Tomato_YellowLeaf__Curl_Virus': {
            'name': 'Yellow Leaf Curl Virus',
            'description': 'Transmitted by whiteflies, causes serious economic losses.',
            'symptoms': 'Yellowing of leaves, curling, stunted growth, reduced fruit production',
            'treatment': 'Control whiteflies with insecticides, remove infected plants',
            'prevention': 'Control whiteflies, use resistant varieties, reflective mulch'
        },
        'Tomato_Bacterial_spot': {
            'name': 'Bacterial Spot',
            'description': 'Caused by Xanthomonas bacteria species.',
            'symptoms': 'Water-soaked spots on leaves and fruits with yellow halo',
            'treatment': 'Apply copper-based bactericides, remove infected material, improve air flow',
            'prevention': 'Use disease-free seeds, avoid overhead watering, practice crop rotation'
        },
        'Potato_healthy': {
            'name': 'Healthy Potato',
            'description': 'The plant appears to be healthy with no visible signs of disease.',
            'symptoms': 'No symptoms - plant is thriving',
            'treatment': 'Continue regular care and maintenance',
            'prevention': 'Maintain proper watering, sunlight, and soil conditions'
        },
        'Potato___Early_blight': {
            'name': 'Early Blight',
            'description': 'Fungal disease caused by Alternaria solani.',
            'symptoms': 'Brown spots with concentric rings on lower leaves, progresses upward',
            'treatment': 'Remove infected foliage, apply mancozeb or chlorothalonil',
            'prevention': 'Use certified seed, mulch, crop rotation, avoid overhead irrigation'
        },
        'Potato___Late_blight': {
            'name': 'Late Blight',
            'description': 'Serious disease caused by Phytophthora infestans, can destroy crops rapidly.',
            'symptoms': 'Water-soaked spots on leaves and stems, white mold on undersides, rapid spread',
            'treatment': 'Apply metalaxyl, mancozeb, or copper fungicides regularly',
            'prevention': 'Use resistant varieties, proper hilling, adequate spacing, avoid overhead watering'
        },
        'Potato___healthy': {
            'name': 'Healthy Potato',
            'description': 'The plant appears to be healthy with no visible signs of disease.',
            'symptoms': 'No symptoms - plant is thriving',
            'treatment': 'Continue regular care and maintenance',
            'prevention': 'Maintain proper watering, sunlight, and soil conditions'
        },
        'Pepper__bell___healthy': {
            'name': 'Healthy Pepper',
            'description': 'The plant appears to be healthy with no visible signs of disease.',
            'symptoms': 'No symptoms - plant is thriving',
            'treatment': 'Continue regular care and maintenance',
            'prevention': 'Maintain proper watering, sunlight, and soil conditions'
        },
        'Pepper__bell___Bacterial_spot': {
            'name': 'Bacterial Spot',
            'description': 'Caused by Xanthomonas species bacteria.',
            'symptoms': 'Small water-soaked dark spots on leaves with yellow halo',
            'treatment': 'Apply copper-based bactericides, remove infected leaves',
            'prevention': 'Use disease-free seeds, avoid overhead watering, practice rotation'
        }
    }

    return disease_database.get(disease_name, {
        'name': disease_name,
        'description': 'Disease information not available',
        'symptoms': 'Please consult with a plant pathologist',
        'treatment': 'Consult with agricultural experts',
        'prevention': 'Practice good crop management'
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File is too large. Maximum size is 16MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
