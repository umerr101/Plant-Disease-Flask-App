"""
Utility functions for Plant Disease Classification System
"""

import os
import json
from pathlib import Path
from datetime import datetime
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


FEATURE_IMAGE_SIZE = (16, 16)
FEATURE_HIST_BINS = 16


def validate_image(image_path):
    """
    Validate if an image file is valid

    Args:
        image_path: Path to the image file

    Returns:
        tuple: (is_valid, message)
    """
    try:
        img = Image.open(image_path)
        img.verify()
        return True, "Image is valid"
    except Exception as e:
        return False, f"Invalid image: {str(e)}"


def is_leaf_image(image_path, green_ratio_threshold=0.12):
    """
    Heuristic check to determine whether an image likely contains a leaf.

    This is a lightweight test that computes the fraction of pixels that are
    predominantly green (green channel stronger than red and blue by a margin).

    Args:
        image_path: Path to the image file
        green_ratio_threshold: Fraction of pixels that must be "green" to
            consider the image a leaf image (default 0.12 = 12%)

    Returns:
        bool: True if image likely contains a leaf, False otherwise
    """
    try:
        img = Image.open(image_path).convert('RGB')
        arr = np.asarray(img, dtype=np.float32) / 255.0

        # compute simple green-pixel mask: G noticeably larger than R and B
        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        # condition: green is greater than both red and blue by a factor
        green_mask = (g > 1.05 * r) & (g > 1.05 * b) & (g > 0.12)

        green_fraction = float(np.count_nonzero(
            green_mask)) / (arr.shape[0] * arr.shape[1])

        return green_fraction >= float(green_ratio_threshold)
    except Exception:
        # If anything goes wrong, be conservative and return False
        return False


def get_image_info(image_path):
    """
    Get information about an image

    Args:
        image_path: Path to the image file

    Returns:
        dict: Image information (size, format, mode)
    """
    try:
        img = Image.open(image_path)
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode,
            'size_kb': os.path.getsize(image_path) / 1024
        }
    except Exception as e:
        return {'error': str(e)}


def resize_image(image_path, size=(128, 128), output_path=None):
    """
    Resize an image to specified dimensions

    Args:
        image_path: Path to input image
        size: Target size as (width, height)
        output_path: Path to save resized image (optional)

    Returns:
        PIL.Image: Resized image
    """
    try:
        img = Image.open(image_path).convert('RGB')
        resized = img.resize(size, Image.Resampling.LANCZOS)

        if output_path:
            resized.save(output_path)

        return resized
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None


def extract_image_features(image_path, image_size=FEATURE_IMAGE_SIZE, hist_bins=FEATURE_HIST_BINS):
    """
    Convert an image into a compact numeric feature vector.

    The vector combines a small resized RGB flattening with per-channel histograms,
    which keeps the model lightweight enough for Python 3.13-compatible scikit-learn.
    """
    img = Image.open(image_path).convert('RGB')
    img = img.resize(image_size, Image.Resampling.LANCZOS)
    image_array = np.asarray(img, dtype=np.float32) / 255.0

    flattened = image_array.reshape(-1)
    histogram_features = []
    for channel_index in range(3):
        channel_histogram, _ = np.histogram(
            image_array[:, :, channel_index],
            bins=hist_bins,
            range=(0.0, 1.0),
            density=True,
        )
        histogram_features.append(channel_histogram.astype(np.float32))

    return np.concatenate([flattened, *histogram_features]).astype(np.float32)


def list_image_files(directory):
    """Return a sorted list of image files in a directory tree."""
    directory = Path(directory)
    valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}
    files = []
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            files.append(file_path)
    return sorted(files)


def load_feature_dataset(split_dir, class_names):
    """
    Load a dataset split from a class-folder structure and return features/labels.
    """
    split_dir = Path(split_dir)
    features = []
    labels = []

    for class_name in class_names:
        class_dir = split_dir / class_name
        if not class_dir.exists():
            continue

        for image_path in list_image_files(class_dir):
            try:
                features.append(extract_image_features(image_path))
                labels.append(class_name)
            except Exception as exc:
                print(f"Skipping {image_path}: {exc}")

    if not features:
        return np.empty((0, 0), dtype=np.float32), []

    return np.vstack(features).astype(np.float32), labels


def normalize_image(image_array):
    """
    Normalize image array to 0-1 range

    Args:
        image_array: NumPy array of image

    Returns:
        np.ndarray: Normalized array
    """
    return image_array.astype(np.float32) / 255.0


def denormalize_image(image_array):
    """
    Denormalize image array from 0-1 range to 0-255

    Args:
        image_array: NumPy array of normalized image

    Returns:
        np.ndarray: Denormalized array
    """
    return (image_array * 255).astype(np.uint8)


def batch_images(image_paths, batch_size=32):
    """
    Create batches from a list of image paths

    Args:
        image_paths: List of image paths
        batch_size: Size of each batch

    Yields:
        list: Batch of image paths
    """
    for i in range(0, len(image_paths), batch_size):
        yield image_paths[i:i + batch_size]


def save_predictions(predictions, output_file='predictions.json'):
    """
    Save predictions to JSON file

    Args:
        predictions: List of prediction results
        output_file: Output file path
    """
    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=2)


def load_predictions(input_file='predictions.json'):
    """
    Load predictions from JSON file

    Args:
        input_file: Input file path

    Returns:
        list: Loaded predictions
    """
    with open(input_file, 'r') as f:
        return json.load(f)


def create_confusion_matrix_plot(cm, class_names, output_path='confusion_matrix.png'):
    """
    Create and save confusion matrix plot

    Args:
        cm: Confusion matrix (numpy array)
        class_names: List of class names
        output_path: Path to save the plot
    """
    plt.figure(figsize=(12, 10))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()

    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45, ha='right')
    plt.yticks(tick_marks, class_names)

    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to {output_path}")


def cleanup_uploads(days=7):
    """
    Clean up old uploaded files

    Args:
        days: Delete files older than this many days
    """
    upload_dir = Path('./uploads')
    current_time = datetime.now().timestamp()
    deleted = 0

    for file in upload_dir.glob('*'):
        if file.is_file():
            file_time = file.stat().st_mtime
            if (current_time - file_time) > (days * 86400):  # seconds per day
                file.unlink()
                deleted += 1

    print(f"Cleaned up {deleted} old files")
    return deleted


def get_dataset_stats(dataset_dir):
    """
    Get statistics about the dataset

    Args:
        dataset_dir: Path to dataset directory

    Returns:
        dict: Dataset statistics
    """
    stats = {
        'total_images': 0,
        'train_images': 0,
        'val_images': 0,
        'test_images': 0,
        'classes': {}
    }

    for split in ['train', 'validation', 'test']:
        split_dir = Path(dataset_dir) / split
        if split_dir.exists():
            count = 0
            for class_dir in split_dir.iterdir():
                if class_dir.is_dir():
                    class_count = len(list(class_dir.glob('*')))
                    count += class_count
                    if class_dir.name not in stats['classes']:
                        stats['classes'][class_dir.name] = {}
                    stats['classes'][class_dir.name][split] = class_count

            stats[f'{split}_images'] = count
            stats['total_images'] += count

    return stats


def print_dataset_stats(stats):
    """
    Pretty print dataset statistics

    Args:
        stats: Dictionary of statistics
    """
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)
    print(f"Total Images: {stats['total_images']:,}")
    print(f"  - Training: {stats['train_images']:,}")
    print(f"  - Validation: {stats['val_images']:,}")
    print(f"  - Test: {stats['test_images']:,}")
    print(f"\nTotal Classes: {len(stats['classes'])}")
    print("\nClass Distribution:")

    for class_name in sorted(stats['classes'].keys()):
        print(f"\n  {class_name}")
        for split, count in stats['classes'][class_name].items():
            print(f"    - {split}: {count}")
    print("\n" + "="*60 + "\n")


def check_system_requirements():
    """
    Check if system meets minimum requirements

    Returns:
        dict: System check results
    """
    import sys
    import psutil

    disk_root = Path.cwd().anchor or str(Path.cwd().drive) + '\\'

    results = {
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'python_ok': sys.version_info >= (3, 13),
        'ram_gb': psutil.virtual_memory().total / (1024**3),
        'ram_ok': psutil.virtual_memory().total / (1024**3) >= 8,
        'disk_gb': psutil.disk_usage(disk_root).total / (1024**3),
        'disk_ok': psutil.disk_usage(disk_root).free / (1024**3) >= 3
    }

    print("\n" + "="*60)
    print("SYSTEM REQUIREMENTS CHECK")
    print("="*60)
    print(
        f"Python Version: {results['python_version']} {'✓' if results['python_ok'] else '✗'}")
    print(f"  Required: 3.13+")
    print(
        f"\nRAM: {results['ram_gb']:.1f} GB {'✓' if results['ram_ok'] else '✗'}")
    print(f"  Recommended: 8GB+")
    print(
        f"\nDisk Free: {results['disk_gb']:.1f} GB {'✓' if results['disk_ok'] else '✗'}")
    print(f"  Required: 3GB+")
    print("\n" + "="*60 + "\n")

    return results


if __name__ == '__main__':
    # Example usage
    print("Plant Disease Classification System - Utilities")
    print("\nThis module contains helper functions.")
    print("Import it in your scripts: from utils import *")
