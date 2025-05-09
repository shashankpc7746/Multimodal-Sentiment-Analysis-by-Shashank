import pickle
import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter  # For checking label distribution

# --- Scikit-learn imports ---
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils.class_weight import compute_class_weight

# --- TensorFlow/Keras imports ---
import tensorflow as tf
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.layers import Input, Dense, Concatenate, Dropout # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore

# +++ Add import for plotting +++
import matplotlib.pyplot as plt
# --- End Add ---

print(f"Using TensorFlow version: {tf.__version__}")

# ------------------ Load Features ------------------
print("\n--- Loading Features ---")
try:
    with open('data/mini_dataset/mini_audio_features.pkl', 'rb') as f:
        audio_features = pickle.load(f)
    print(f"✅ audio_features loaded: {len(audio_features)} entries")

    with open('data/mini_dataset/mini_video_features.pkl', 'rb') as f:
        video_features = pickle.load(f)
    print(f"✅ video_features loaded: {len(video_features)} entries")

    with open('data/mini_dataset/mini_text_features.pkl', 'rb') as f:
        text_features = pickle.load(f)
    print(f"✅ text_features loaded: {len(text_features)} entries")

    df = pd.read_csv('data/processed_dataset.csv')
    print(f"🟡 Rows in CSV: {len(df)}")

except FileNotFoundError as e:
    print(f"❌ Error loading data files: {e}")
    exit()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit()

# ------------------ Match and Prepare Data ------------------
print("\n--- Matching Features and Labels ---")
audio_data, video_data, text_data, labels = [], [], [], []

required_columns = ['video_id', 'clip_id', 'annotation']
if not all(col in df.columns for col in required_columns):
    print(f"❌ CSV missing required columns: {required_columns}")
    exit()

for _, row in df.iterrows():
    try:
        key = f"{row['video_id']}_{int(row['clip_id'])}"
    except:
        continue
    if key in audio_features and key in video_features and key in text_features:
        audio_data.append(np.asarray(audio_features[key]))
        video_data.append(np.asarray(video_features[key]))
        text_data.append(np.asarray(text_features[key]))
        labels.append(row['annotation'])

print(f"🟢 Total matched clips: {len(labels)}")
print("📊 Label distribution:", Counter(labels))

# ------------------ Encode Labels ------------------
print("\n--- Encoding Labels ---")
le = LabelEncoder()
y_int = le.fit_transform(labels)
y = to_categorical(y_int)
num_classes = len(le.classes_)

# ------------------ Stack Features ------------------
X_a = np.stack(audio_data)
X_v = np.stack(video_data)
X_t = np.stack(text_data)
print(f"🔢 Feature shapes: Audio={X_a.shape}, Video={X_v.shape}, Text={X_t.shape}, Labels={y.shape}")

# ------------------ Compute Class Weights ------------------
class_weights = compute_class_weight('balanced', classes=np.unique(y_int), y=y_int)
class_weight_dict = dict(enumerate(class_weights))
print("⚖️ Class weights:", class_weight_dict)

# ------------------ Train/Test Split ------------------
X_a_train, X_a_test, X_v_train, X_v_test, X_t_train, X_t_test, y_train, y_test = train_test_split(
    X_a, X_v, X_t, y, test_size=0.2, random_state=42, stratify=y_int
)

# ------------------ Scale Features ------------------
scaler_a, scaler_v, scaler_t = StandardScaler(), StandardScaler(), StandardScaler()
X_a_train = scaler_a.fit_transform(X_a_train)
X_v_train = scaler_v.fit_transform(X_v_train)
X_t_train = scaler_t.fit_transform(X_t_train)
X_a_test = scaler_a.transform(X_a_test)
X_v_test = scaler_v.transform(X_v_test)
X_t_test = scaler_t.transform(X_t_test)

# In multimodal_model.py, after fitting/applying scalers:

print("\n--- Saving Scalers ---")
with open('models/scaler_audio.pkl', 'wb') as f:
    pickle.dump(scaler_a, f)
print("💾 Audio scaler saved to models/scaler_audio.pkl")

with open('models/scaler_video.pkl', 'wb') as f:
    pickle.dump(scaler_v, f)
print("💾 Video scaler saved to models/scaler_video.pkl")

with open('models/scaler_text.pkl', 'wb') as f:
    pickle.dump(scaler_t, f)
print("💾 Text scaler saved to models/scaler_text.pkl")

# ------------------ Build Sub-networks ------------------
print("\n--- Building Model Architecture ---")
def build_ffnn(dim, prefix):
    inp = Input(shape=(dim,), name=f"{prefix}_in")
    x = Dense(64, activation='relu', name=f"{prefix}_dense")(inp)
    x = Dropout(0.3, name=f"{prefix}_drop")(x)
    return inp, x

inp_a, out_a = build_ffnn(X_a_train.shape[1], 'audio')
inp_v, out_v = build_ffnn(X_v_train.shape[1], 'video')
inp_t, out_t = build_ffnn(X_t_train.shape[1], 'text')

# ------------------ Fusion and Final Model ------------------
merged = Concatenate(name='fusion_concat')([out_a, out_v, out_t])
x = Dense(64, activation='relu', name='fusion_dense')(merged)
x = Dropout(0.3, name='fusion_drop')(x)
# Output logits without softmax
tokens = Dense(num_classes, activation=None, name='output_logits')(x)

model = Model(inputs=[inp_a, inp_v, inp_t], outputs=tokens)
model.compile(
    optimizer=Adam(0.0005),
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)
print("✅ Model compiled.\n")
model.summary()

# ------------------ Train ------------------
print("\n--- Training ---")
eh = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model.fit(
    [X_a_train, X_v_train, X_t_train], y_train,
    validation_split=0.1, epochs=100, batch_size=32,
    class_weight=class_weight_dict, callbacks=[eh]
)

# ------------------ Evaluate ------------------
print("\n--- Evaluating ---")
loss, acc = model.evaluate([X_a_test, X_v_test, X_t_test], y_test)
print(f"Test loss: {loss:.4f}, Test acc: {acc:.4f}")

y_pred = model.predict([X_a_test, X_v_test, X_t_test])
y_pred_labels = np.argmax(y_pred, axis=1)
y_true_labels = np.argmax(y_test, axis=1)

print(classification_report(y_true_labels, y_pred_labels, target_names=le.classes_))
cm = confusion_matrix(y_true_labels, y_pred_labels)
Disp = ConfusionMatrixDisplay(cm, display_labels=le.classes_)
plt.figure(figsize=(6,5))
Disp.plot(ax=plt.gca())
plt.title('Confusion Matrix')
plt.show()

# ------------------ Save Model + Encoder ------------------
model.save('models/final_multimodal_logits_model.h5')
with open('models/label_encoder.pkl','wb') as f:
    pickle.dump(le, f)
print("💾 Model & encoder saved.")