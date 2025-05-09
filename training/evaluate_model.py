# training/evaluate_model.py

import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load processed features
def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

print("🔄 Loading test features...")

audio_data = load_pickle('data/mini_dataset/mini_audio_features.pkl')
video_data = load_pickle('data/mini_dataset/mini_video_features.pkl')
text_data = load_pickle('data/mini_dataset/mini_text_features.pkl')

X_audio_test = np.array(audio_data['test'])
X_video_test = np.array(video_data['test'])
X_text_test = np.array(text_data['test'])

y_test = np.array(audio_data['test_labels'])  # Assumes all labels are the same across modalities

print("✅ Features loaded successfully.")

# Load trained multimodal model
print("🔄 Loading trained model...")
model_path = '../models/multimodal_sentiment_model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")
    
model = load_model(model_path)
print("✅ Model loaded.")

# Predict
print("🔄 Running predictions on test data...")
pred_probs = model.predict([X_audio_test, X_video_test, X_text_test])
y_pred = np.argmax(pred_probs, axis=1)

# Evaluation Metrics
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Neutral', 'Positive']))

print("📉 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Neutral', 'Positive'],
            yticklabels=['Negative', 'Neutral', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()
