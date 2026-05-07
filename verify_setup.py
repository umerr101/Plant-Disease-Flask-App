"""
System check and verification script
Run this before training the model to ensure everything is set up correctly
"""

import sys
import os
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_check(name, status, message=""):
    """Print check result"""
    symbol = "✓" if status else "✗"
    print(f"  {symbol} {name}")
    if message:
        print(f"    {message}")


def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")

    major, minor, micro = sys.version_info[:3]
    version_string = f"{major}.{minor}.{micro}"

    print(f"  Current: Python {version_string}")
    print(f"  Required: Python 3.13+")

    is_valid = sys.version_info >= (3, 13)
    print_check("Version compatibility", is_valid)

    return is_valid


def check_dependencies():
    """Check if required packages are installed"""
    print_header("Dependency Check")

    required_packages = {
        'joblib': 'Joblib (Model Serialization)',
        'flask': 'Flask (Web Framework)',
        'numpy': 'NumPy (Numerical Computing)',
        'pandas': 'Pandas (Data Processing)',
        'PIL': 'Pillow (Image Processing)',
        'sklearn': 'Scikit-learn (ML Tools)',
        'matplotlib': 'Matplotlib (Visualization)',
        'psutil': 'Psutil (System Checks)',
    }

    missing = []
    installed = []

    for package, full_name in required_packages.items():
        try:
            __import__(package)
            print_check(full_name, True)
            installed.append(package)
        except ImportError:
            print_check(full_name, False,
                        "Run: pip install -r requirements.txt")
            missing.append(package)

    return len(missing) == 0, missing


def check_directories():
    """Check if required directories exist"""
    print_header("Directory Structure Check")

    base_dir = Path(__file__).parent
    required_dirs = {
        'dataset/train': 'Training images',
        'dataset/validation': 'Validation images',
        'dataset/test': 'Test images',
        'templates': 'Web templates',
        'models': 'Model storage',
        'uploads': 'Upload storage',
    }

    missing = []
    for dir_path, description in required_dirs.items():
        full_path = base_dir / dir_path
        exists = full_path.exists()
        print_check(f"{description} ({dir_path})", exists)
        if not exists:
            missing.append(dir_path)

    return len(missing) == 0, missing


def check_files():
    """Check if required files exist"""
    print_header("File Existence Check")

    base_dir = Path(__file__).resolve().parent
    required_files = {
        'app.py': 'Flask application',
        'train_model.py': 'Training script',
        'config.py': 'Configuration',
        'utils.py': 'Utility functions',
        'requirements.txt': 'Dependencies list',
        'templates/index.html': 'Home page',
        'templates/about.html': 'About page',
    }

    missing = []
    for file_path, description in required_files.items():
        full_path = base_dir / file_path
        exists = full_path.exists()
        print_check(f"{description} ({file_path})", exists)
        if not exists:
            missing.append(file_path)

    return len(missing) == 0, missing


def check_dataset():
    """Check dataset contents"""
    print_header("Dataset Contents Check")

    base_dir = Path(__file__).resolve().parent
    dataset_dir = base_dir / 'dataset'

    stats = {
        'train': 0,
        'validation': 0,
        'test': 0
    }

    classes_found = set()

    for split in stats.keys():
        split_dir = dataset_dir / split
        if split_dir.exists():
            for class_dir in split_dir.iterdir():
                if class_dir.is_dir():
                    image_count = len(list(class_dir.glob('*')))
                    stats[split] += image_count
                    classes_found.add(class_dir.name)

    print(f"\n  Dataset Statistics:")
    print(f"    Training images: {stats['train']:,}")
    print(f"    Validation images: {stats['validation']:,}")
    print(f"    Test images: {stats['test']:,}")
    print(f"    Total images: {sum(stats.values()):,}")
    print(f"    Unique classes: {len(classes_found)}")

    has_data = sum(stats.values()) > 0
    print_check("Dataset contains images", has_data)

    if classes_found:
        print(f"\n  Found classes:")
        for class_name in sorted(classes_found):
            print(f"    - {class_name}")

    return has_data


def check_resources():
    """Check system resources"""
    print_header("System Resources Check")

    try:
        import psutil
        disk_root = Path.cwd().anchor or str(Path.cwd().drive) + '\\'

        # RAM
        ram_total = psutil.virtual_memory().total / (1024**3)
        ram_free = psutil.virtual_memory().available / (1024**3)
        print(f"  RAM: {ram_total:.1f} GB total, {ram_free:.1f} GB available")
        print_check("Sufficient RAM (8GB+)", ram_total >= 8)

        # Disk
        disk_total = psutil.disk_usage(disk_root).total / (1024**3)
        disk_free = psutil.disk_usage(disk_root).free / (1024**3)
        print(f"  Disk: {disk_total:.1f} GB total, {disk_free:.1f} GB free")
        print_check("Sufficient disk space (3GB+)", disk_free >= 3)

        # CPU
        cpu_count = psutil.cpu_count()
        print(f"  CPU: {cpu_count} cores")
        print_check("Multi-core processor", cpu_count >= 2)

    except ImportError:
        print("  Warning: psutil not installed, skipping resource check")
        print("  Install with: pip install psutil")


def check_port():
    """Check if port 5000 is available"""
    print_header("Port Availability Check")

    import socket

    port = 5000
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            print_check(f"Port {port} is available", True)
            return True
    except OSError:
        print_check(f"Port {port} is available", False,
                    f"Port {port} is already in use. Change port in app.py")
        return False


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Plant Disease Classification System - Setup Verification".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

    results = {
        'Python Version': check_python_version(),
        'Port Check': check_port(),
    }

    deps_ok, missing_deps = check_dependencies()
    results['Dependencies'] = deps_ok

    dirs_ok, missing_dirs = check_directories()
    results['Directories'] = dirs_ok

    files_ok, missing_files = check_files()
    results['Files'] = files_ok

    dataset_ok = check_dataset()
    results['Dataset'] = dataset_ok

    check_resources()

    # Summary
    print_header("Summary")

    all_ok = all(results.values())

    for check_name, status in results.items():
        print_check(check_name, status)

    print("\n")

    if all_ok and dataset_ok:
        print("  ✓ All checks passed!")
        print("\n  Next steps:")
        print("    1. Run: python train_model.py")
        print("    2. Wait for training to complete (2-4 hours)")
        print("    3. Run: python app.py")
        print("    4. Open browser to: http://localhost:5000")
        return 0
    else:
        print("  ✗ Some checks failed!")
        print("\n  Issues to fix:")

        if missing_deps:
            print(f"    - Install missing packages: pip install -r requirements.txt")

        if missing_dirs:
            print(
                f"    - Create missing directories: {', '.join(missing_dirs)}")

        if missing_files:
            print(f"    - Missing files: {', '.join(missing_files)}")

        if not dataset_ok:
            print(f"    - Dataset not found or empty")
            print(f"    - Ensure dataset folder has train/validation/test subdirectories")

        print("\n  For more information, see README.md")
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n  Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n  Error during verification: {e}")
        sys.exit(1)
