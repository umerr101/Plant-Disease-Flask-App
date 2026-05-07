# 📋 Project File Index

## Complete File Structure and Descriptions

```
ann project/
├── 🐍 Core Application Files
│   ├── app.py                    - Flask web server (12 KB)
│   ├── train_model.py            - Model training script (8 KB)
│   ├── config.py                 - Configuration file (6 KB)
│   └── utils.py                  - Utility functions (7 KB)
│
├── 🌐 Web Interface
│   └── templates/
│       ├── index.html            - Home page with upload (15 KB)
│       └── about.html            - Information page (12 KB)
│
├── ⚙️ Setup & Configuration
│   ├── requirements.txt          - Python dependencies (0.3 KB)
│   ├── run.bat                   - Windows quick start (4 KB)
│   ├── run.sh                    - Linux/Mac quick start (3 KB)
│   ├── verify_setup.py           - Setup verification (8 KB)
│   └── .gitignore                - Git ignore file (2 KB)
│
├── 📚 Documentation
│   ├── README.md                 - Full documentation (15 KB)
│   ├── QUICKSTART.md             - Quick start guide (8 KB)
│   ├── IMPLEMENTATION_SUMMARY.md - This project summary (12 KB)
│   ├── FILE_INDEX.md             - File descriptions (THIS FILE)
│   └── Report.docx               - Original project report (283 KB)
│
├── 📁 Data & Model Folders
│   ├── models/                   - Trained models (created after training)
│   ├── uploads/                  - User uploads (auto-managed)
│   └── dataset/                  - PlantVillage dataset (2 GB)
│       ├── train/                - Training images (70%)
│       ├── validation/           - Validation images (10%)
│       └── test/                 - Test images (20%)
│
└── 📊 Output Files (Created After Training)
    ├── models/plant_disease_model.h5    - Trained neural network (200 MB)
    ├── models/class_names.pkl           - Disease class labels (1 KB)
    └── models/training_history.png      - Training plots (500 KB)
```

---

## 🐍 Core Application Files

### 1. **app.py** - Flask Web Server

- **Lines:** ~500
- **Size:** 12 KB
- **Purpose:** Main Flask application
- **Key Components:**
  - Flask app initialization
  - Image upload handler
  - Model loading and prediction
  - REST API endpoints
  - Error handling
  - Disease information database
- **Key Routes:**
  - `GET /` → Home page
  - `GET /about` → About page
  - `POST /api/predict` → Make prediction
  - `GET /api/health` → Health check
- **Run:** `python app.py`
- **Access:** http://localhost:5000

---

### 2. **train_model.py** - Model Training Script

- **Lines:** ~350
- **Size:** 8 KB
- **Purpose:** Train the Feedforward Neural Network
- **Key Functions:**
  - `create_train_val_test_generators()` - Data loading
  - `build_fnn_model(num_classes)` - Model creation
  - `train_model()` - Main training function
- **Inputs:**
  - PlantVillage dataset from `dataset/` folder
  - Configuration from `config.py`
- **Outputs:**
  - `models/plant_disease_model.h5` (trained model)
  - `models/class_names.pkl` (class labels)
  - `models/training_history.png` (plots)
- **Runtime:** 2-4 hours (first time)
- **Run:** `python train_model.py`

---

### 3. **config.py** - Configuration File

- **Lines:** ~200
- **Size:** 6 KB
- **Purpose:** Centralized configuration management
- **Sections:**
  - File paths (BASE_DIR, MODELS_PATH, etc.)
  - Image processing (IMG_SIZE=128)
  - Model training (BATCH_SIZE=32, EPOCHS=20)
  - Flask configuration (HOST, PORT, MAX_UPLOAD)
  - Data augmentation settings
  - Disease information database
- **Usage:** `from config import *`
- **Editable:** Yes (customize hyperparameters)

---

### 4. **utils.py** - Utility Functions

- **Lines:** ~300
- **Size:** 7 KB
- **Purpose:** Helper functions
- **Key Functions:**
  - `validate_image()` - Verify image files
  - `get_image_info()` - Extract image metadata
  - `resize_image()` - Resize images
  - `normalize_image()` - Normalize pixel values
  - `get_dataset_stats()` - Dataset statistics
  - `check_system_requirements()` - System check
  - `create_confusion_matrix_plot()` - Visualization
- **Usage:** `from utils import validate_image, get_dataset_stats`

---

## 🌐 Web Interface Files

### 5. **templates/index.html** - Home Page

- **Lines:** ~600
- **Size:** 15 KB
- **Purpose:** Main user interface
- **Sections:**
  - Header with navigation
  - Image upload area (drag & drop)
  - Image preview section
  - Prediction results display
  - Disease information section
  - Footer
- **Styling:** Embedded CSS (responsive, mobile-friendly)
- **JavaScript:** Embedded (image upload, API calls, UI updates)
- **Features:**
  - Real-time image preview
  - Confidence visualization
  - Top 5 predictions display
  - Detailed disease info
  - Error handling

---

### 6. **templates/about.html** - Information Page

- **Lines:** ~400
- **Size:** 12 KB
- **Purpose:** Project documentation
- **Sections:**
  - Project overview
  - Problem statement
  - Solution description
  - Features (cards)
  - Methodology (5 steps)
  - Technology stack
  - Dataset information
  - Expected results
  - Limitations and future work
  - Getting started
- **Styling:** Embedded CSS (matching index.html)

---

## ⚙️ Setup & Configuration Files

### 7. **requirements.txt** - Python Dependencies

- **Lines:** 9
- **Size:** 0.3 KB
- **Format:** pip requirements format
- **Packages:**
  ```
  flask==2.3.3
  tensorflow==2.14.0
  keras==2.14.0
  numpy==1.24.3
  pandas==2.0.3
  pillow==10.0.0
  scikit-learn==1.3.0
  matplotlib==3.7.2
  werkzeug==2.3.7
  ```
- **Install:** `pip install -r requirements.txt`

---

### 8. **run.bat** - Windows Quick Start

- **Lines:** ~120
- **Size:** 4 KB
- **Purpose:** Automated setup for Windows
- **Features:**
  - Python version check
  - Virtual environment creation
  - Dependency installation
  - Interactive menu
  - Model training option
  - Application launch
- **Usage:** Double-click or `run.bat` in CMD
- **Platform:** Windows only

---

### 9. **run.sh** - Linux/Mac Quick Start

- **Lines:** ~100
- **Size:** 3 KB
- **Purpose:** Automated setup for Linux/Mac
- **Features:**
  - Python version check
  - Virtual environment creation
  - Dependency installation
  - Interactive menu
  - Model training option
  - Application launch
- **Usage:** `chmod +x run.sh && ./run.sh`
- **Platform:** Linux and macOS

---

### 10. **verify_setup.py** - Setup Verification

- **Lines:** ~400
- **Size:** 8 KB
- **Purpose:** Verify system is ready
- **Checks:**
  - Python version (3.13+)
  - Required packages
  - Directory structure
  - File existence
  - Dataset contents
  - System resources (RAM, disk)
  - Port availability
- **Run:** `python verify_setup.py`
- **Exit Codes:** 0 (success), 1 (failure)

---

### 11. **.gitignore** - Git Ignore

- **Lines:** ~80
- **Size:** 2 KB
- **Purpose:** Exclude files from Git
- **Excludes:**
  - Python cache (`__pycache__/`)
  - Virtual environments (`venv/`)
  - IDE settings (`.vscode/`, `.idea/`)
  - Trained models (too large)
  - Dataset files (too large)
  - User uploads
  - Log files
  - Temporary files

---

## 📚 Documentation Files

### 12. **README.md** - Full Documentation

- **Lines:** ~700
- **Size:** 15 KB
- **Sections:**
  1. Project overview
  2. Problem statement
  3. Dataset description
  4. Technology stack
  5. Project structure
  6. Installation guide
  7. Usage guide
  8. Model architecture
  9. API endpoints
  10. Expected performance
  11. Limitations
  12. Future improvements
  13. Troubleshooting
  14. Resources
- **Format:** Markdown with code examples
- **Audience:** Developers and users

---

### 13. **QUICKSTART.md** - Quick Start Guide

- **Lines:** ~300
- **Size:** 8 KB
- **Purpose:** Get started in 5 minutes
- **Sections:**
  - Windows setup (2 steps)
  - Linux/Mac setup (2 steps)
  - Manual setup
  - Training explanation
  - Web app usage
  - Troubleshooting (8 common issues)
  - Advanced usage
- **Format:** Markdown with code blocks
- **Audience:** First-time users

---

### 14. **IMPLEMENTATION_SUMMARY.md** - Project Summary

- **Lines:** ~550
- **Size:** 12 KB
- **Purpose:** Overview of all files created
- **Sections:**
  - Files created (with descriptions)
  - How to get started
  - Model architecture
  - Expected performance
  - Supported classes
  - API examples
  - Configuration options
  - Checklist
  - Learning outcomes
- **Format:** Markdown with tables and lists
- **Audience:** Project overview

---

### 15. **FILE_INDEX.md** - File Descriptions

- **This File**
- **Lines:** ~800
- **Size:** 20 KB
- **Purpose:** Complete file reference
- **Includes:**
  - File structure diagram
  - Detailed descriptions
  - File sizes
  - Key features
  - Usage instructions
  - Code examples
  - Related files

---

### 16. **Report.docx** - Original Project Report

- **Format:** Microsoft Word (.docx)
- **Size:** 283 KB
- **Content:**
  - Project title and metadata
  - Abstract
  - Introduction
  - Problem statement
  - Literature review
  - Methodology (5 steps)
  - Implementation plan
  - Expected results
  - Limitations and future work
  - Conclusion
- **Read with:** Microsoft Word or compatible reader

---

## 📁 Data & Model Folders

### 17. **models/** - Model Storage Directory

- **Purpose:** Store trained neural network
- **Created:** After running `python train_model.py`
- **Contents (after training):**
  - `plant_disease_model.h5` (~200 MB) - Trained FNN
  - `class_names.pkl` (~1 KB) - Class labels
  - `training_history.png` (~500 KB) - Plots
- **Auto-created:** Yes (by train_model.py)
- **Manual creation:** Not needed

---

### 18. **uploads/** - Upload Directory

- **Purpose:** Store user uploaded images
- **Auto-managed:** Yes
- **Cleanup:** Old files deleted periodically
- **Size:** Typically a few MB
- **Auto-created:** Yes (by Flask app)

---

### 19. **dataset/** - PlantVillage Dataset

- **Purpose:** Train/validate/test images
- **Structure:**
  ```
  dataset/
  ├── train/        (70% of images) ~38,000 images
  ├── validation/   (10% of images) ~5,400 images
  └── test/         (20% of images) ~10,800 images
  ```
- **Classes:** 15 total
- **Total Size:** ~2 GB
- **Format:** JPEG images
- **Source:** PlantVillage Dataset (Open source)
- **Manual creation:** Required (download separately)

---

## 📊 Output Files (Generated After Training)

### plant_disease_model.h5

- **Format:** HDF5 (TensorFlow/Keras model)
- **Size:** ~200 MB
- **Content:** Trained neural network weights and architecture
- **Created:** By `python train_model.py`
- **Used by:** `app.py` for predictions
- **Keep:** Yes (required for predictions)

### class_names.pkl

- **Format:** Python pickle
- **Size:** ~1 KB
- **Content:** List of 15 disease class names
- **Created:** By `python train_model.py`
- **Used by:** `app.py` for labels
- **Keep:** Yes (required for labels)

### training_history.png

- **Format:** PNG image
- **Size:** ~500 KB
- **Content:** Accuracy and loss plots
- **Created:** By `python train_model.py`
- **Reference:** Check training progress visually
- **Keep:** Optional (for reference)

---

## 🔍 File Dependencies

```
app.py
├── requires: config.py
├── requires: templates/index.html
├── requires: templates/about.html
├── requires: models/plant_disease_model.h5 (after training)
├── requires: models/class_names.pkl (after training)
└── imports: Flask, TensorFlow, Keras, Pillow, etc.

train_model.py
├── requires: config.py
├── requires: dataset/train/
├── requires: dataset/validation/
├── requires: dataset/test/
├── creates: models/plant_disease_model.h5
├── creates: models/class_names.pkl
├── creates: models/training_history.png
└── imports: TensorFlow, NumPy, Pandas, etc.

verify_setup.py
├── requires: app.py
├── requires: train_model.py
├── requires: config.py
├── requires: templates/ directory
├── requires: dataset/ directory (recommended)
└── imports: sys, pathlib, socket, etc.

templates/index.html
├── imports: JavaScript (embedded)
├── imports: CSS (embedded)
└── depends on: /api/predict endpoint

templates/about.html
├── imports: CSS (embedded)
└── standalone (no API dependencies)
```

---

## 📊 File Size Summary

| Category       | Files  | Total Size |
| -------------- | ------ | ---------- |
| Python Code    | 4      | 33 KB      |
| HTML Templates | 2      | 27 KB      |
| Documentation  | 4      | 50 KB      |
| Configuration  | 4      | 8 KB       |
| **Total**      | **14** | **118 KB** |

_Plus: 2 GB dataset + 200 MB model (created after training)_

---

## ✅ File Checklist

Before running the application:

### Essential Files

- [x] app.py
- [x] train_model.py
- [x] config.py
- [x] requirements.txt
- [x] templates/index.html
- [x] templates/about.html

### Setup Files

- [x] run.bat (Windows users)
- [x] run.sh (Linux/Mac users)
- [x] verify_setup.py

### Documentation Files

- [x] README.md
- [x] QUICKSTART.md
- [x] IMPLEMENTATION_SUMMARY.md
- [x] FILE_INDEX.md
- [x] Report.docx

### Required Folders

- [x] dataset/train/ (must have images)
- [x] dataset/validation/ (must have images)
- [x] dataset/test/ (must have images)

### Created by Application

- [x] models/ (created automatically)
- [x] uploads/ (created automatically)

---

## 🚀 Quick Reference

### To Get Started

```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### To Verify Setup

```bash
python verify_setup.py
```

### To Train Model

```bash
python train_model.py
```

### To Run Application

```bash
python app.py
```

### To Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📞 File Navigation Guide

**"I want to..."**

| Goal                       | File to Edit                       |
| -------------------------- | ---------------------------------- |
| Change model architecture  | config.py (HIDDEN_LAYERS)          |
| Change training parameters | config.py (BATCH_SIZE, EPOCHS)     |
| Add more disease info      | app.py (get_disease_info function) |
| Modify upload limit        | config.py (MAX_CONTENT_LENGTH)     |
| Change Flask port          | app.py or config.py (PORT)         |
| Update styling             | templates/index.html or about.html |
| Change image size          | config.py (IMG_SIZE)               |
| Read full docs             | README.md                          |
| Quick start                | QUICKSTART.md                      |

---

## 📚 Related Documentation

- **Full Reference:** [README.md](README.md)
- **Quick Guide:** [QUICKSTART.md](QUICKSTART.md)
- **Project Summary:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Original Report:** Report.docx

---

**Last Updated:** May 7, 2026
**Total Files:** 16 core files + directories
**Ready for:** Training and deployment
