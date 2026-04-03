import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Step 1: Load dataset (example with a few classes for speed)
data_dir = r"C:\Users\HP\Downloads\Food 101\food-101\food-101\images"
classes = ["pizza", "hamburger", "sushi"]  # pick a few classes first
X, y = [], []

import os

print("Dataset path exists:", os.path.exists(data_dir))
print("Pizza folder exists:", os.path.exists(os.path.join(data_dir, "pizza")))

classes = ["pizza", "hamburger", "sushi"]

for label, food in enumerate(classes):
    path = os.path.join(data_dir, food)
    for img_name in os.listdir(path)[:500]:  # limit to 500 per class
        img_path = os.path.join(path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is None:
            continue
        img = cv2.resize(img, (128, 128))
        X.append(img)
        y.append(label)

X = np.array(X) / 255.0
y = to_categorical(np.array(y))

print("Dataset shape:", X.shape, y.shape)

# Step 2: Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Build CNN model
model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(128,128,3)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(len(classes), activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Step 4: Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Step 5: Evaluate
loss, acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", acc)

# Step 6: Calorie estimation (simple mapping)
calorie_map = {"pizza": 285, "hamburger": 354, "sushi": 200}  # avg calories per serving

# Predict on one image
test_img = cv2.imread(r"C:\Users\HP\Downloads\food-101\images\pizza\pizza1.jpg")
test_img = cv2.resize(test_img, (128,128)) / 255.0
test_img = np.expand_dims(test_img, axis=0)

pred_class = np.argmax(model.predict(test_img))
food_item = classes[pred_class]
print("Predicted food:", food_item)
print("Estimated calories:", calorie_map[food_item])
