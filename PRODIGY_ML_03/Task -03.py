import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# Path to the dataset folder
data_dir = r"C:\Users\HP\Downloads\Dogs vs Cats\dogs-vs-cats"
categories = ["cat", "dog"]

X, y = [], []

for category in categories:
    path = os.path.join(data_dir, category)
    label = categories.index(category)  # 0 = cat, 1 = dog

    for img_name in os.listdir(path)[:500]:  # limit to 500 per class for speed
        img_path = os.path.join(path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            print("Failed to load:", img_path)
            continue
        img = cv2.resize(img, (64, 64))
        X.append(img.flatten())
        y.append(label)

X = np.array(X)
y = np.array(y)
print("Dataset shape:", X.shape, y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = SVC(kernel="linear", random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=categories))
