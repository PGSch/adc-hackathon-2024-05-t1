#!/bin/bash

# Clean previous builds
rm -rf build dist *.egg-info

# Build the package
python3 setup.py bdist_wheel

# Force reinstall the package
pip install --force-reinstall dist/adchackathon202405t1-0.0.7-py3-none-any.whl

# Run the module
python3 -m src --file_name "inventory_manager.py" --class_or_method "InventoryManager"
