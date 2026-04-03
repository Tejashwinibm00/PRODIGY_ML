import os
import cv2
import numpy as np

DATA_DIR = r"C:\Users\HP\Downloads\Hand gesture\leapGestRecog"
print("Dataset path exists:", os.path.exists(DATA_DIR))

# Quick test: load one image
test_path = os.path.join(DATA_DIR, '00', '01_palm', 'frame_00_01_0001.png')
print("Test image path:", test_path, "exists:", os.path.exists(test_path))
if os.path.exists(test_path):
    img = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)
    print("Image shape:", img.shape if img is not None else "None")
else:
    print("Test image not found")

print("Packages imported successfully")