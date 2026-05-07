# Plant Disease Classification System

A Flask-based web application that uses Artificial Neural Networks (ANN) to classify plant diseases from leaf images. The system is trained on the PlantVillage dataset and can identify 15 different plant disease conditions with high accuracy.

## 📋 Project Overview

This project implements a Feedforward Neural Network (FNN) to automate plant disease detection from leaf images. It provides a fast, low-cost, and accessible solution for early disease detection in agriculture, reducing the need for expert pathologists and expensive laboratory tests.

**Key Features:**
- 🤖 AI-powered disease classification using FNN
- 📸 Real-time image analysis
- 💡 Detailed disease information and treatment recommendations
- 🌐 User-friendly web interface
- 📊 Confidence scores for predictions
- 🔒 Secure file upload handling

## 🎯 Problem Statement

Plant diseases devastate crops worldwide, yet traditional detection methods are slow, costly, and expert-dependent. This system addresses the need for an automatic, reliable, and accessible disease detection tool.

## 📊 Dataset

**PlantVillage Dataset** - Contains 54,000+ labeled images of healthy and diseased plant leaves

**Supported Classes (15 total):**

### Tomato (11 classes)
- Tomato Early Blight
- Tomato Late Blight
- Tomato Leaf Mold
- Tomato Septoria Leaf Spot
- Tomato Bacterial Spot
- Tomato Spider Mites
- Tomato Target Spot
- Tomato Mosaic Virus
- Tomato Yellow Leaf Curl Virus
- Tomato Healthy

### Potato (4 classes)
- Potato Early Blight
- Potato Late Blight
- Potato Healthy

### Pepper Bell (2 classes)
- Pepper Bacterial Spot
- Pepper Healthy

## 🛠️ Technology Stack

- **Framework:** Flask 2.3.3
- **Deep Learning:** TensorFlow/Keras 2.14.0
- **Data Processing:** NumPy, Pandas, Pillow
- **ML Libraries:** Scikit-learn
- **Visualization:** Matplotlib
- **Python Version:** 3.13+

## 📁 Project Structure

```
ann project/
├── app.py                      # Flask application
├── train_model.py              # Model training script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── models/                     # Trained model storage
│   ├── plant_disease_model.h5 # Trained FNN model
│   ├── class_names.pkl        # Class labels
│   └── training_history.png   # Training plots
├── templates/                  # HTML templates
│   ├── index.html             # Home page
│   └── about.html             # About page
├── uploads/                    # User uploaded images
└── dataset/                    # PlantVillage dataset
    ├── train/                 # Training images
    ├── validation/            # Validation images
    └── test/                  # Test images
```

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.13 or higher
- pip package manager
- Sufficient disk space for dataset (≈2GB) and model (≈200MB)

### 2. Installation

**Step 1: Clone/Download the project**
```bash
cd "C:\Users\HP\OneDrive\Desktop\ann project"
```

**Step 2: Create virtual environment (optional but recommended)**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

### 3. Training the Model

**Important:** The model must be trained before using the Flask application.

```bash
python train_model.py
```

This script will:
- Load the PlantVillage dataset from the `dataset/` folder
- Preprocess and augment the images
- Build and compile the FNN model
- Train for 20 epochs
- Evaluate on the test set
- Save the trained model and class names

**Expected Training Time:** 2-4 hours (depends on your hardware)

**Outputs:**
- `models/plant_disease_model.h5` - Trained model
- `models/class_names.pkl` - Class labels
- `models/training_history.png` - Training plots

### 4. Running the Flask Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

**Output:**
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

Open your browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

1. **Navigate to Home Page:** Visit `http://localhost:5000`

2. **Upload Image:** 
   - Click "Select Image" button or drag and drop
   - Supported formats: PNG, JPG, JPEG, GIF, BMP
   - Maximum file size: 16MB

3. **Get Prediction:**
   - The AI model analyzes the image (2-5 seconds)
   - Displays predicted disease with confidence score
   - Shows top 5 alternative predictions

4. **Review Disease Information:**
   - **Description:** Overview of the disease
   - **Symptoms:** Visual signs of the disease
   - **Treatment:** Recommended interventions
   - **Prevention:** Preventive measures

5. **New Prediction:** Click "New Prediction" to analyze another image

## 🔬 Model Architecture

**Feedforward Neural Network (FNN)**

```
Input Layer:          49,152 neurons (128×128×3 flattened image)
    ↓
Hidden Layer 1:       512 neurons, ReLU activation, Dropout(0.3)
    ↓
Hidden Layer 2:       256 neurons, ReLU activation, Dropout(0.3)
    ↓
Hidden Layer 3:       128 neurons, ReLU activation, Dropout(0.2)
    ↓
Hidden Layer 4:       64 neurons, ReLU activation, Dropout(0.2)
    ↓
Output Layer:         15 neurons, Softmax activation
                      (one per disease class)
```

**Training Configuration:**
- **Loss Function:** Categorical Cross-entropy
- **Optimizer:** Adam (learning rate: 0.001)
- **Batch Size:** 32
- **Epochs:** 20
- **Data Augmentation:** Yes (rotation, flip, shift, zoom)
- **Train/Val/Test Split:** 70% / 10% / 20%

## 📊 Expected Performance

After training, the model should achieve:
- **Test Accuracy:** 85-92%
- **Precision:** 85-90% per class
- **Recall:** 85-90% per class

*Note: Actual performance may vary depending on hardware and data preprocessing*

## 🔧 API Endpoints

### 1. Home Page
```
GET /
```
Returns the main application interface.

### 2. About Page
```
GET /about
```
Returns project information and documentation.

### 3. Health Check
```
GET /api/health
```
Returns model status and available classes.

**Response Example:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 15,
  "classes": ["Tomato_Bacterial_spot", "Tomato_Early_blight", ...]
}
```

### 4. Prediction
```
POST /api/predict
```
Accepts image file and returns disease prediction.

**Request:**
- Form Data: `file` (image file)

**Response Example:**
```json
{
  "success": true,
  "predicted_disease": "Tomato_Early_blight",
  "confidence": 0.94,
  "confidence_percentage": "94.23%",
  "all_predictions": [
    {"class": "Tomato_Early_blight", "confidence": 0.94},
    {"class": "Tomato_Healthy", "confidence": 0.03},
    ...
  ],
  "disease_info": {
    "name": "Early Blight",
    "description": "...",
    "symptoms": "...",
    "treatment": "...",
    "prevention": "..."
  },
  "upload_filename": "leaf.jpg"
}
```

## ⚠️ Limitations

- **Image Quality Sensitive:** Requires clear, well-lit photos
- **Lower than CNN:** FNN accuracy is less than Convolutional Neural Networks
- **Similar Diseases:** May confuse visually similar diseases
- **Controlled Conditions:** Works best on images similar to training data
- **Single Disease:** Detects one primary disease; may miss multiple infections

## 🔮 Future Improvements

- [ ] Migrate to CNN architecture
- [ ] Mobile app development
- [ ] Real-time camera feed support
- [ ] Expand dataset with more crop varieties
- [ ] IoT sensor integration
- [ ] Multi-disease detection
- [ ] Ensemble methods
- [ ] Multi-language support
- [ ] Offline mode capability
- [ ] Disease severity classification

## 📝 Configuration

### Image Processing
Edit `train_model.py` and `app.py` to modify:
```python
IMG_SIZE = 128              # Image dimensions
BATCH_SIZE = 32             # Batch size for training
EPOCHS = 20                 # Number of training epochs
```

### Flask Configuration
Edit `app.py` to modify:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
```

### Model Upload Folder
```python
app.config['UPLOAD_FOLDER'] = 'uploads'  # Uploaded images storage
```

## 🐛 Troubleshooting

### Issue: "Model not loaded"
**Solution:** Run `python train_model.py` to train the model first.

### Issue: "ModuleNotFoundError"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "Memory Error" during training
**Solution:** Reduce `BATCH_SIZE` in `train_model.py`

### Issue: Low prediction accuracy
**Solutions:**
- Ensure good image quality
- Adjust preprocessing in `train_model.py`
- Check if image is similar to training data
- Consider retraining with more epochs

### Issue: Application crashes
**Solution:** Check Flask logs and ensure:
- Port 5000 is available
- Dataset folder exists
- Models folder has trained model

## 📚 Resources

- **PlantVillage Dataset:** https://plantvillage.org/
- **TensorFlow Docs:** https://www.tensorflow.org/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Keras Guide:** https://keras.io/

## 📄 License

This project is for educational purposes. The PlantVillage dataset is available under CC0 1.0 Universal.

## 👥 Authors

- **Student:** Umer Khalil
- **Registration:** 23108194
- **Course:** Artificial Neural Network
- **Department:** Robotics & Artificial Intelligence
- **Submitted to:** Mr. Hasaan Mujtaba

## 📞 Support

For issues, questions, or suggestions, please refer to the project documentation or contact your instructor.

## 📋 Project Report

For detailed methodology, results, and analysis, please see the included `Report.docx` document.

---

**Last Updated:** May 2026
**Version:** 1.0.0
