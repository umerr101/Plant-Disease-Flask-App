"""
Configuration file for the Plant Disease Classification System
"""

import os
from pathlib import Path

# ==================== File Paths ====================
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / 'dataset'
MODELS_PATH = BASE_DIR / 'models'
UPLOADS_PATH = BASE_DIR / 'uploads'
TEMPLATES_PATH = BASE_DIR / 'templates'

# Create directories if they don't exist
for directory in [MODELS_PATH, UPLOADS_PATH]:
    directory.mkdir(exist_ok=True)

# ==================== Image Processing ====================
IMG_SIZE = 128  # Image resize dimension (128x128)
IMG_CHANNELS = 3  # RGB channels

# ==================== Model Training ====================
BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.1
TEST_SPLIT = 0.1

# Model architecture
HIDDEN_LAYERS = [512, 256, 128, 64]  # Number of neurons in each hidden layer
ACTIVATION = 'relu'  # Activation function for hidden layers
DROPOUT_RATES = [0.3, 0.3, 0.2, 0.2]  # Dropout rate for each hidden layer

# Training parameters
LEARNING_RATE = 0.001
OPTIMIZER = 'adam'  # 'adam' or 'sgd'
LOSS_FUNCTION = 'categorical_crossentropy'

# ==================== Data Augmentation ====================
AUGMENTATION_CONFIG = {
    'rotation_range': 20,
    'width_shift_range': 0.2,
    'height_shift_range': 0.2,
    'shear_range': 0.2,
    'zoom_range': 0.2,
    'horizontal_flip': True,
    'fill_mode': 'nearest'
}

# ==================== Flask Configuration ====================
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
HOST = '0.0.0.0'
PORT = 5000

# File upload configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# ==================== Model Paths ====================
MODEL_PATH = MODELS_PATH / 'plant_disease_model.h5'
CLASS_NAMES_PATH = MODELS_PATH / 'class_names.pkl'
TRAINING_HISTORY_PATH = MODELS_PATH / 'training_history.png'

# ==================== Disease Information ====================
# Database of plant diseases with detailed information
DISEASE_DATABASE = {
    'Tomato_healthy': {
        'name': 'Healthy Tomato',
        'severity': 'None',
        'description': 'The plant appears to be healthy with no visible signs of disease.'
    },
    'Tomato_Early_blight': {
        'name': 'Early Blight',
        'severity': 'High',
        'description': 'Fungal disease caused by Alternaria tomatophila'
    },
    'Tomato_Late_blight': {
        'name': 'Late Blight',
        'severity': 'Critical',
        'description': 'Serious disease caused by Phytophthora infestans'
    },
    'Tomato_Leaf_Mold': {
        'name': 'Leaf Mold',
        'severity': 'Medium',
        'description': 'Caused by Passalora fulva'
    },
    'Tomato_Septoria_leaf_spot': {
        'name': 'Septoria Leaf Spot',
        'severity': 'Medium',
        'description': 'Caused by Septoria lycopersici'
    },
    'Tomato_Spider_mites_Two_spotted_spider_mite': {
        'name': 'Spider Mites',
        'severity': 'High',
        'description': 'Pest damage from two-spotted spider mites'
    },
    'Tomato__Target_Spot': {
        'name': 'Target Spot',
        'severity': 'High',
        'description': 'Caused by Corynespora cassiicola'
    },
    'Tomato__Tomato_mosaic_virus': {
        'name': 'Tomato Mosaic Virus',
        'severity': 'High',
        'description': 'Viral disease spread by contact'
    },
    'Tomato__Tomato_YellowLeaf__Curl_Virus': {
        'name': 'Yellow Leaf Curl Virus',
        'severity': 'Critical',
        'description': 'Transmitted by whiteflies'
    },
    'Tomato_Bacterial_spot': {
        'name': 'Bacterial Spot',
        'severity': 'Medium',
        'description': 'Caused by Xanthomonas bacteria'
    },
    'Potato_healthy': {
        'name': 'Healthy Potato',
        'severity': 'None',
        'description': 'The plant appears healthy'
    },
    'Potato___Early_blight': {
        'name': 'Early Blight',
        'severity': 'High',
        'description': 'Fungal disease caused by Alternaria solani'
    },
    'Potato___Late_blight': {
        'name': 'Late Blight',
        'severity': 'Critical',
        'description': 'Serious disease caused by Phytophthora infestans'
    },
    'Pepper__bell___healthy': {
        'name': 'Healthy Pepper',
        'severity': 'None',
        'description': 'The plant appears healthy'
    },
    'Pepper__bell___Bacterial_spot': {
        'name': 'Bacterial Spot',
        'severity': 'Medium',
        'description': 'Caused by Xanthomonas species'
    }
}

# ==================== Logging ====================
LOG_LEVEL = 'INFO'
LOG_FILE = BASE_DIR / 'logs' / 'app.log'
LOG_FILE.parent.mkdir(exist_ok=True)

# ==================== Performance Metrics ====================
EXPECTED_ACCURACY = 0.85  # Expected minimum test accuracy (85%)
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for valid predictions

if __name__ == '__main__':
    print("Configuration Loaded Successfully!")
    print(f"Base Directory: {BASE_DIR}")
    print(f"Dataset Path: {DATASET_PATH}")
    print(f"Models Path: {MODELS_PATH}")
    print(f"Image Size: {IMG_SIZE}x{IMG_SIZE}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Epochs: {EPOCHS}")
