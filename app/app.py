# app/app.py

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
from tensorflow.keras.models import load_model # type: ignore
import tensorflow as tf # +++ ADDED TENSORFLOW IMPORT +++

# Preprocessing utilities
# from preprocessing.extract_frames import extract_frames # Uncomment if extract_all_video_features needs it
from preprocessing.extract_all_video_features import extract_all_video_features
from preprocessing.extract_audio import extract_audio
from preprocessing.extract_all_audio_features import extract_mfcc_features
from preprocessing.transcribe_audio import transcribe_audio
from preprocessing.extract_all_text_features import extract_text_features

st.set_page_config(page_title="Multimodal Sentiment Classifier", layout="wide", initial_sidebar_state="collapsed")
st.title("🎬 Multimodal Sentiment Classifier")
st.markdown("Upload a short video clip (e.g., 5-15 seconds) to analyze its sentiment.")

@st.cache_resource
def load_all_models_and_scalers():
    model_path = "models/final_multimodal_logits_model.h5"
    le_path = "models/label_encoder.pkl"
    sa_path, sv_path, st_path = "models/scaler_audio.pkl", "models/scaler_video.pkl", "models/scaler_text.pkl"

    if not all(os.path.exists(p) for p in [model_path, le_path, sa_path, sv_path, st_path]):
        st.error("🔴 Critical Error: One or more model/scaler files are missing. Please ensure all model files are in the 'models' directory.")
        st.stop()

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

model, le, scaler_a, scaler_v, scaler_t = load_all_models_and_scalers()

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    # --- USE COLUMNS FOR LAYOUT ---
    col_video, col_results = st.columns([0.6, 0.4]) # 60% for video, 40% for results

    with col_video: # Column for video display
        st.subheader("📽️ Your Uploaded Video")
        st.video(uploaded_file)

    with col_results: # Column for processing status and results
        with st.spinner("⚙️ Analyzing video... This might take a moment..."):
            vid_path = None
            audio_wav_path = None
            analysis_successful = False # Flag to track if we get to prediction
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_vid_file:
                    tmp_vid_file.write(uploaded_file.read())
                    vid_path = tmp_vid_file.name

                video_feat_raw = extract_all_video_features(vid_path)
                if video_feat_raw is None:
                    st.error("❌ Could not extract video features.")
                    st.stop()
                video_feat_scaled = scaler_v.transform(video_feat_raw.reshape(1, -1))[0]

                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
                    audio_wav_path = tmp_audio_file.name
                
                if not extract_audio(vid_path, audio_wav_path):
                    st.error("❌ Could not extract audio from video.")
                    st.stop()

                mfcc_vec_raw = extract_mfcc_features(audio_wav_path)
                if mfcc_vec_raw is None:
                    st.error("❌ Could not extract audio MFCC features.")
                    st.stop()
                mfcc_vec_scaled = scaler_a.transform(mfcc_vec_raw.reshape(1, -1))[0]

                transcript = transcribe_audio(audio_wav_path)
                text_feat_scaled = np.zeros(768)
                
                if transcript:
                    text_feat_raw = extract_text_features(transcript)
                    if text_feat_raw is None:
                        st.warning("⚠️ Could extract transcript, but not text features. Using zero vector for text.")
                    else:
                        text_feat_scaled = scaler_t.transform(text_feat_raw.reshape(1, -1))[0]
                else:
                    st.warning("⚠️ Could not transcribe audio or transcript is empty. Using zero vector for text.")

                X_vid = np.expand_dims(video_feat_scaled, 0)
                X_aud = np.expand_dims(mfcc_vec_scaled, 0)
                X_txt = np.expand_dims(text_feat_scaled, 0)

                preds = model.predict([X_aud, X_vid, X_txt])
                idx = np.argmax(preds, axis=1)[0]
                sentiment = le.inverse_transform([idx])[0]
                
                probabilities = tf.nn.softmax(preds[0]).numpy()
                prob_dict = {label: prob for label, prob in zip(le.classes_, probabilities)}
                analysis_successful = True

            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                import traceback
                st.error(f"Traceback: {traceback.format_exc()}")
                # No st.stop() here, finally block will still run
            finally:
                if vid_path and os.path.exists(vid_path):
                    os.remove(vid_path)
                if audio_wav_path and os.path.exists(audio_wav_path):
                    os.remove(audio_wav_path)
        
        # Display results in the results column
        if analysis_successful:
            st.success("✅ Analysis Complete!")
            st.subheader("📊 Analysis Results")
            
            sentiment_color = "gray" # Default for Neutral or other
            if sentiment == "Positive": sentiment_color = "green"
            elif sentiment == "Negative": sentiment_color = "red"
            
            st.markdown(f"### Predicted Sentiment: <span style='color:{sentiment_color}; font-weight:bold;'>{sentiment}</span>", unsafe_allow_html=True)

            if transcript:
                st.markdown(f"**📝 Transcript:**")
                st.markdown(f"> _{transcript}_") # Using blockquote for transcript
            else:
                st.markdown("_No transcript was available for text analysis._")

            st.markdown("---")
            st.markdown("**Confidence Scores:**")
            for label, prob_val in prob_dict.items():
                st.markdown(f"- **{label}:** {prob_val:.2%}")
        # else: (Handled by st.error within the try block)
        #    st.error("Analysis could not be completed due to an error.")

else:
    st.info("☝️ Upload a video to get started!")

st.markdown("---")
st.markdown("Created by Shashank | Powered by Multimodal AI")