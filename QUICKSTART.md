# Quick Start Guide

## ⚡ 5-Minute Setup

### For Windows Users:

1. **Double-click `run.bat`**
   - This will automatically set up everything for you

2. **Choose option 1: Train the Model**
   - First time only - takes 2-4 hours
   - This trains the neural network on your dataset

3. **Choose option 2: Run the Application**
   - Starts the Flask web server
   - Open browser to `http://localhost:5000`

### For Linux/Mac Users:

1. **Run in terminal:**

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

2. **Choose option 1: Train the Model**
3. **Choose option 2: Run the Application**

---

## 🔍 Manual Setup (If Scripts Don't Work)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
python train_model.py
```

- **Duration:** 2-4 hours (first time only)
- **Requires:** PlantVillage dataset in `dataset/` folder
- **Creates:**
  - `models/plant_disease_model.h5` (trained model)
  - `models/class_names.pkl` (disease classes)
  - `models/training_history.png` (accuracy plots)

### Step 3: Run the Application

```bash
python app.py
```

- **Opens:** http://localhost:5000
- **Press:** CTRL+C to stop

---

## 📊 What Happens During Training?

```
Loading dataset...
├── Reading 54,000+ images
├── Splitting into train/val/test
└── Applying augmentation

Building model...
├── Input layer: 49,152 neurons
├── Hidden layers: 512 → 256 → 128 → 64
└── Output layer: 15 disease classes

Training starts...
├── Epoch 1/20: loss=2.5, accuracy=0.65
├── Epoch 5/20: loss=0.8, accuracy=0.82
├── Epoch 10/20: loss=0.3, accuracy=0.90
└── Epoch 20/20: loss=0.15, accuracy=0.94

Evaluation...
├── Test Accuracy: 94.23%
├── Precision: 93.8%
├── Recall: 94.1%
└── Confusion Matrix: [Generated]

Saving model...
└── Models saved to models/ folder ✓
```

---

## 🌐 Using the Web Application

### Upload Image

1. Click **"Select Image"** button
2. Or **drag & drop** an image
3. Supported formats: PNG, JPG, JPEG, GIF, BMP
4. Max size: 16MB

### Get Prediction

- AI analyzes image (2-5 seconds)
- Shows predicted disease
- Displays confidence score
- Lists top 5 alternative predictions

### View Disease Info

- **Description:** What the disease is
- **Symptoms:** Visual signs to look for
- **Treatment:** How to treat it
- **Prevention:** How to prevent it

### New Prediction

Click **"New Prediction"** to analyze another image

---

## 📁 Project Structure

```
ann project/
├── app.py                 ← Run this for Flask app
├── train_model.py         ← Run this to train model
├── config.py              ← Configuration settings
├── requirements.txt       ← Dependencies list
├── README.md              ← Full documentation
├── run.bat                ← Windows quick start
├── run.sh                 ← Linux/Mac quick start
│
├── models/                ← Trained models (created after training)
│   ├── plant_disease_model.h5
│   ├── class_names.pkl
│   └── training_history.png
│
├── templates/             ← Web interface
│   ├── index.html
│   └── about.html
│
├── uploads/               ← User uploaded images
│
└── dataset/               ← Plant images (PlantVillage)
    ├── train/
    ├── validation/
    └── test/
```

---

## ⚙️ System Requirements

- **Python:** 3.13+
- **RAM:** 8GB+ recommended
- **GPU:** Optional (NVIDIA GPU for faster training)
- **Disk:** 3GB+ (dataset + model + OS)
- **Processor:** Dual-core 2.0GHz+

---

## 🐛 Troubleshooting

### "Model not loaded" Error

**Solution:** Train the model first

```bash
python train_model.py
```

### "Module not found" Error

**Solution:** Install dependencies

```bash
pip install -r requirements.txt
```

### Port 5000 Already in Use

**Solution:** Edit `app.py`, change `port=5000` to `port=5001`

### "Out of memory" During Training

**Solution:** Reduce batch size in `config.py`:

```python
BATCH_SIZE = 16  # Instead of 32
```

### Low Prediction Accuracy

**Solutions:**

- Use clear, well-lit photos
- Ensure leaves fill most of the image
- Try different angles/lighting
- Retrain with more epochs

---

## 📈 Expected Results

After training completes:

- ✅ Model saved to `models/` folder
- ✅ Test accuracy: 85-92%
- ✅ Training plots saved
- ✅ Ready to use Flask app

### Performance by Crop:

- **Tomato:** 92-95% accuracy
- **Potato:** 88-92% accuracy
- **Pepper:** 85-90% accuracy

---

## 🚀 Advanced Usage

### Run with Custom Configuration

Edit `config.py` before training:

```python
EPOCHS = 30              # Train longer
BATCH_SIZE = 16         # Smaller batches
LEARNING_RATE = 0.0001  # Slower learning
```

### Use GPU Acceleration

Install CUDA-enabled TensorFlow:

```bash
pip install tensorflow[and-cuda]
```

### Run on Different Port

Edit `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

### Enable Logging

Add to `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📞 Need Help?

1. **Read:** Full README.md for detailed documentation
2. **Check:** Report.docx for project details
3. **Review:** config.py for configuration options
4. **Reference:** app.py and train_model.py for code

---

**Ready? Start with `run.bat` (Windows) or `run.sh` (Linux/Mac)** ✨
