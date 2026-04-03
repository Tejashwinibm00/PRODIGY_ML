import os
import tensorflow as tf
print(tf.__version__)
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Stop verbose tensorflow warnings (optional)
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')

# Step 1: Load dataset
DATA_DIR = r"C:\Users\HP\Downloads\Hand gesture\leapGestRecog"  # adjust if different

print("Dataset path exists:", os.path.exists(DATA_DIR))
if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Dataset path not found: {DATA_DIR}")

# Supported image extensions
image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

# First scan for gesture class names from nested folders
gesture_names = set()
for root, dirs, files in os.walk(DATA_DIR):
    # we expect gesture class at the immediate parent of the image files, e.g. .../00/01_palm/file.jpg
    if root == DATA_DIR:
        continue
    # if root is a gesture folder (contains image files), extract gesture name
    if any(f.lower().endswith(tuple(image_extensions)) for f in files):
        gesture_names.add(os.path.basename(root))

if not gesture_names:
    raise ValueError("No gesture image folders found. Check directory structure under " + DATA_DIR)

gesture_names = sorted(list(gesture_names))
label_map = {g: i for i, g in enumerate(gesture_names)}
print("Found gesture classes:", gesture_names)

X, y = [], []
total_images = 0
max_images = 2000  # limit for quick testing
for root, dirs, files in os.walk(DATA_DIR):
    for fname in files:
        if total_images >= max_images:
            break
        ext = os.path.splitext(fname)[1].lower()
        if ext not in image_extensions:
            continue
        gesture_label = os.path.basename(root)
        if gesture_label not in label_map:
            continue
        img_path = os.path.join(root, fname)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print("Warning: failed to read", img_path)
            continue
        img = cv2.resize(img, (64, 64))
        X.append(img)
        y.append(label_map[gesture_label])
        total_images += 1
        if total_images % 500 == 0:
            print(f"Loaded {total_images} images...")
    if total_images >= max_images:
        break

print(f"Total images loaded: {total_images}")

if len(X) == 0:
    raise RuntimeError("No images loaded. Check that gesture images are present and readable.")

X = np.array(X, dtype='float32').reshape(-1, 64, 64, 1) / 255.0

y = to_categorical(np.array(y), num_classes=len(gesture_names))
print("Dataset shape:", X.shape, y.shape)

# Step 2: Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

# Step 3: Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(len(gesture_names), activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Step 4: Train model
print("Starting training...")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Step 5: Evaluate
loss, acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", acc)

