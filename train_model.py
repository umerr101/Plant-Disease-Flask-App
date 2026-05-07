"""
Train the Feedforward Neural Network for Plant Disease Classification
"""

import os
from pathlib import Path
import pickle

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings

from utils import load_feature_dataset

# Configuration
DATASET_PATH = Path('./dataset')
MODEL_PATH = Path('./models/plant_disease_model.joblib')
CLASS_NAMES_PATH = Path('./models/class_names.pkl')
TRAINING_HISTORY_PATH = Path('./models/training_history.png')


def get_class_names():
    """Get all disease classes from training directory"""
    train_dir = DATASET_PATH / 'train'
    return sorted([d.name for d in train_dir.iterdir() if d.is_dir()])


def load_split(split_name, class_names):
    """Load one split into feature and label arrays."""
    split_dir = DATASET_PATH / split_name
    return load_feature_dataset(split_dir, class_names)


def build_fnn_model():
    """Build a scikit-learn feedforward neural network pipeline."""
    return Pipeline([
        ('scaler', StandardScaler()),
        ('mlp', MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            solver='adam',
            alpha=1e-4,
            batch_size=128,
            learning_rate_init=0.001,
            max_iter=50,
            early_stopping=False,
            verbose=True,
            random_state=42,
        )),
    ])


def train_model():
    """Train the FNN model"""

    print("Loading datasets...")
    class_names = get_class_names()
    train_features, train_labels = load_split('train', class_names)
    val_features, val_labels = load_split('validation', class_names)
    test_features, test_labels = load_split('test', class_names)

    if train_features.size == 0:
        raise RuntimeError(
            'No training images found. Check the dataset/train folder.')

    print(f"Training samples: {len(train_labels)}")
    print(f"Validation samples: {len(val_labels)}")
    print(f"Test samples: {len(test_labels)}")
    print(f"Classes: {class_names}")

    label_encoder = LabelEncoder()
    label_encoder.fit(class_names)
    y_train = label_encoder.transform(train_labels)
    y_val = label_encoder.transform(val_labels)
    y_test = label_encoder.transform(test_labels)

    print("\nBuilding model...")
    model = build_fnn_model()

    print("\nTraining model...")
    warnings.filterwarnings('ignore', category=ConvergenceWarning)
    model.fit(train_features, y_train)

    train_predictions = model.predict(train_features)
    val_predictions = model.predict(val_features) if len(
        val_labels) else np.array([])
    test_predictions = model.predict(test_features)

    train_accuracy = accuracy_score(y_train, train_predictions)
    val_accuracy = accuracy_score(y_val, val_predictions) if len(
        val_labels) else float('nan')
    test_accuracy = accuracy_score(y_test, test_predictions)

    print(f"\nTraining Accuracy: {train_accuracy:.4f}")
    if len(val_labels):
        print(f"Validation Accuracy: {val_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")

    print("\nDetailed Classification Report:")
    print(classification_report(y_test, test_predictions, target_names=class_names))

    precision = precision_score(
        y_test, test_predictions, average='weighted', zero_division=0)
    recall = recall_score(y_test, test_predictions,
                          average='weighted', zero_division=0)
    print(f"Weighted Precision: {precision:.4f}")
    print(f"Weighted Recall: {recall:.4f}")

    confusion = confusion_matrix(y_test, test_predictions)

    # Save model and class names
    print("\nSaving model...")
    joblib.dump({
        'pipeline': model,
        'label_encoder_classes': label_encoder.classes_.tolist(),
        'feature_image_size': (16, 16),
        'hist_bins': 16,
    }, MODEL_PATH)

    with open(CLASS_NAMES_PATH, 'wb') as f:
        pickle.dump(class_names, f)

    print("Model and class names saved successfully!")

    # Plot model metrics
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.bar(['Train', 'Validation', 'Test'], [train_accuracy, val_accuracy,
            test_accuracy], color=['#667eea', '#764ba2', '#4caf50'])
    plt.ylim(0, 1)
    plt.title('Accuracy')
    plt.ylabel('Score')

    plt.subplot(1, 2, 2)
    plt.imshow(confusion, interpolation='nearest', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(TRAINING_HISTORY_PATH)
    print("Training history plot saved!")


if __name__ == '__main__':
    # Create models directory
    os.makedirs('./models', exist_ok=True)

    train_model()
