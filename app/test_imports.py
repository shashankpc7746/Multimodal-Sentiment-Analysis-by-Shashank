import sys
import os

# Add project root to Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import tempfile
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf

# Preprocessing utilities
from preprocessing.extract_all_video_features import extract_all_video_features
from preprocessing.extract_audio import extract_audio
from preprocessing.extract_all_audio_features import extract_mfcc_features
from preprocessing.transcribe_audio import transcribe_audio
from preprocessing.extract_all_text_features import extract_text_features

st.set_page_config(page_title="Test App", layout="wide")
st.title("Test Multimodal Sentiment Classifier")

@st.cache_resource
def load_models():
    try:
        model_path = "models/final_multimodal_logits_model.h5"
        le_path = "models/label_encoder.pkl"
        sa_path, sv_path, st_path = "models/scaler_audio.pkl", "models/scaler_video.pkl", "models/scaler_text.pkl"

        if not all(os.path.exists(p) for p in [model_path, le_path, sa_path, sv_path, st_path]):
            st.error("Model files missing")
            return None, None, None, None, None

        model = load_model(model_path)
        with open(le_path, "rb") as f:
            le = pickle.load(f)
        with open(sa_path, "rb") as f:
            scaler_a = pickle.load(f)
        with open(sv_path, "rb") as f:
            scaler_v = pickle.load(f)
        with open(st_path, "rb") as f:
            scaler_t = pickle.load(f)
        return model, le, scaler_a, scaler_v, scaler_t
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None, None, None

model, le, scaler_a, scaler_v, scaler_t = load_models()

if model is None:
    st.error("Failed to load models. Please check your model files.")
    st.stop()

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.video(uploaded_file)

    with col2:
        with st.spinner("Processing..."):
            try:
                # Save video temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    vid_path = tmp_file.name

                # Extract features
                video_feat = extract_all_video_features(vid_path)
                if video_feat is None:
                    st.error("Video feature extraction failed")
                    st.stop()

                video_feat_scaled = scaler_v.transform(video_feat.reshape(1, -1))[0]

                # Extract audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                    audio_path = tmp_audio.name

                if not extract_audio(vid_path, audio_path):
                    st.error("Audio extraction failed")
                    st.stop()

                # Extract audio features
                audio_feat = extract_mfcc_features(audio_path)
                if audio_feat is None:
                    st.error("Audio feature extraction failed")
                    st.stop()

                audio_feat_scaled = scaler_a.transform(audio_feat.reshape(1, -1))[0]

                # Transcribe and extract text features
                transcript = transcribe_audio(audio_path)
                text_feat_scaled = np.zeros(768)

                if transcript:
                    text_feat = extract_text_features(transcript)
                    if text_feat is not None:
                        text_feat_scaled = scaler_t.transform(text_feat.reshape(1, -1))[0]

                # Make prediction
                X_aud = np.expand_dims(audio_feat_scaled, 0)
                X_vid = np.expand_dims(video_feat_scaled, 0)
                X_txt = np.expand_dims(text_feat_scaled, 0)

                preds = model.predict([X_aud, X_vid, X_txt])
                idx = np.argmax(preds, axis=1)[0]
                sentiment = le.inverse_transform([idx])[0]

                probabilities = tf.nn.softmax(preds[0]).numpy()
                prob_dict = {label: prob for label, prob in zip(le.classes_, probabilities)}

                # Display results
                st.success("Analysis Complete!")

                if sentiment == "Positive":
                    st.markdown("### 🟢 Positive Sentiment")
                elif sentiment == "Negative":
                    st.markdown("### 🔴 Negative Sentiment")
                else:
                    st.markdown("### ⚪ Neutral Sentiment")

                if transcript:
                    st.write("**Transcript:**", transcript)

                st.write("**Confidence Scores:**")
                for label, prob in prob_dict.items():
                    st.write(f"- {label}: {prob:.2%}")

                # Cleanup
                os.remove(vid_path)
                os.remove(audio_path)

            except Exception as e:
                st.error(f"Error: {e}")
                import traceback
                st.code(traceback.format_exc())

else:
    st.info("Upload a video to get started!")