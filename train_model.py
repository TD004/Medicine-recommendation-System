import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

# Load the dataset
df = pd.read_csv("Training.csv")

# Separate features and target
X = df.drop(columns=["prognosis"])
y = df["prognosis"]

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Support Vector Classifier (SVC)
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {accuracy * 100:.2f}%")

# Save the model to a file
os.makedirs("models", exist_ok=True)
with open("models/svc.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved to models/svc.pkl")
