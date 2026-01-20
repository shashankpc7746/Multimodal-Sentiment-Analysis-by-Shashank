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
import time
from tensorflow.keras.models import load_model # type: ignore
import tensorflow as tf # +++ ADDED TENSORFLOW IMPORT +++

# Preprocessing utilities
from preprocessing.extract_all_video_features import extract_all_video_features
from preprocessing.extract_audio import extract_audio
from preprocessing.extract_all_audio_features import extract_mfcc_features
from preprocessing.transcribe_audio import transcribe_audio
from preprocessing.extract_all_text_features import extract_text_features

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-bg: #0f172a;
        --secondary-bg: #1e293b;
        --accent-color: #3b82f6;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --success-color: #10b981;
        --error-color: #ef4444;
        --warning-color: #f59e0b;
        --neutral-color: #6b7280;
        --card-bg: #334155;
        --border-color: #475569;
    }

    /* Global styles */
    .main {
        background: linear-gradient(135deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
        color: var(--text-primary);
    }

    /* Header styling */
    .title-container {
        background: linear-gradient(135deg, var(--accent-color), #1d4ed8);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }

    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #bfdbfe;
        margin-bottom: 0;
    }

    /* Card styling */
    .feature-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    .card-title {
        color: var(--accent-color);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Upload area styling */
    .upload-container {
        background: var(--card-bg);
        border: 2px dashed var(--accent-color);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }

    .upload-container:hover {
        border-color: #60a5fa;
        background: rgba(59, 130, 246, 0.05);
    }

    /* Progress and status styling */
    .progress-container {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--accent-color);
    }

    .status-step {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .status-step.processing {
        background: rgba(245, 158, 11, 0.1);
        border-left: 3px solid var(--warning-color);
    }

    .status-step.completed {
        background: rgba(16, 185, 129, 0.1);
        border-left: 3px solid var(--success-color);
    }

    .status-icon {
        margin-right: 0.75rem;
        font-size: 1.2rem;
    }

    /* Results styling */
    .results-container {
        background: linear-gradient(135deg, var(--card-bg), #374151);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid var(--border-color);
    }

    .sentiment-result {
        text-align: center;
        margin: 2rem 0;
    }

    .sentiment-badge {
        display: inline-block;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        animation: pulse 2s infinite;
    }

    .sentiment-positive {
        background: linear-gradient(135deg, var(--success-color), #059669);
        color: white;
    }

    .sentiment-negative {
        background: linear-gradient(135deg, var(--error-color), #dc2626);
        color: white;
    }

    .sentiment-neutral {
        background: linear-gradient(135deg, var(--neutral-color), #4b5563);
        color: white;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Confidence chart styling */
    .confidence-section {
        margin: 2rem 0;
    }

    .confidence-bar {
        display: flex;
        align-items: center;
        margin: 0.75rem 0;
        padding: 0.5rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
    }

    .confidence-label {
        min-width: 80px;
        font-weight: 600;
        margin-right: 1rem;
    }

    .confidence-fill {
        flex: 1;
        height: 24px;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.1);
    }

    .confidence-fill-positive {
        background: linear-gradient(90deg, var(--success-color), #10b981);
    }

    .confidence-fill-negative {
        background: linear-gradient(90deg, var(--error-color), #ef4444);
    }

    .confidence-fill-neutral {
        background: linear-gradient(90deg, var(--neutral-color), #6b7280);
    }

    .confidence-value {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-weight: 600;
        color: white;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }

    /* Transcript styling */
    .transcript-container {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 4px solid var(--accent-color);
    }

    .transcript-text {
        font-style: italic;
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 1.1rem;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        border-top: 1px solid var(--border-color);
    }

    .footer-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }

    /* Sidebar styling */
    .sidebar-content {
        background: var(--secondary-bg);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    .sidebar-title {
        color: var(--accent-color);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
        border: 1px solid var(--border-color);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent-color);
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }

        .title-container {
            padding: 1.5rem;
        }

        .feature-card {
            padding: 1rem;
        }
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="🎬 Multimodal Sentiment Analyzer",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar with information
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-title">🎭 About the Model</div>
        <p style="color: #cbd5e1; margin-bottom: 1rem;">
            This AI analyzes sentiment from video content using three modalities:
            <strong>Video</strong>, <strong>Audio</strong>, and <strong>Text</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Model metrics
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-title">📊 Model Performance</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">76.3%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">0.83</div>
            <div class="metric-label">Positive F1</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">0.71</div>
            <div class="metric-label">Negative F1</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">0.44</div>
            <div class="metric-label">Neutral F1</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-title">🔧 Technologies Used</div>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
            <span style="background: #3b82f6; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">TensorFlow</span>
            <span style="background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">PyTorch</span>
            <span style="background: #f59e0b; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">ResNet18</span>
            <span style="background: #ef4444; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">DistilBERT</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main title section
st.markdown("""
<div class="title-container">
    <h1 class="main-title">🎬 Multimodal Sentiment Analyzer</h1>
    <p class="subtitle">Advanced AI-powered sentiment analysis from video content using visual, audio, and textual cues</p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🎥 Video Analysis</div>
        <p style="color: #cbd5e1; margin: 0;">
            Extracts visual features using ResNet18 CNN to analyze facial expressions, gestures, and body language.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🎵 Audio Analysis</div>
        <p style="color: #cbd5e1; margin: 0;">
            Processes acoustic features using MFCCs to detect tone, pitch, and emotional cues in speech.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">📝 Text Analysis</div>
        <p style="color: #cbd5e1; margin: 0;">
            Leverages DistilBERT embeddings to understand semantic meaning and contextual sentiment in transcribed speech.
        </p>
    </div>
    """, unsafe_allow_html=True)

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

# Upload section
st.markdown("""
<div class="upload-container">
    <h3 style="color: #3b82f6; margin-bottom: 1rem;">📤 Upload Your Video</h3>
    <p style="color: #cbd5e1; margin-bottom: 0;">
        Select a short video clip (5-15 seconds) for sentiment analysis. Supported formats: MP4, MOV, AVI, MKV
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["mp4", "mov", "avi", "mkv"], label_visibility="collapsed")

if uploaded_file:
    # Progress tracking
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    # Initialize progress steps
    steps = [
        {"name": "Video Upload", "status": "completed", "icon": "✅"},
        {"name": "Video Processing", "status": "processing", "icon": "⚙️"},
        {"name": "Audio Extraction", "status": "pending", "icon": "🎵"},
        {"name": "Speech Recognition", "status": "pending", "icon": "🎤"},
        {"name": "Feature Extraction", "status": "pending", "icon": "🧠"},
        {"name": "Sentiment Analysis", "status": "pending", "icon": "📊"},
    ]

    def update_progress(current_step):
        with status_placeholder.container():
            st.markdown("""
            <div class="progress-container">
                <h4 style="color: #3b82f6; margin-bottom: 1rem;">🔄 Analysis Progress</h4>
            </div>
            """, unsafe_allow_html=True)

            for i, step in enumerate(steps):
                if i < current_step:
                    step["status"] = "completed"
                elif i == current_step:
                    step["status"] = "processing"
                else:
                    step["status"] = "pending"

                status_class = f"status-step {step['status']}"
                st.markdown(f"""
                <div class="{status_class}">
                    <span class="status-icon">{step['icon']}</span>
                    <span style="color: #f8fafc;">{step['name']}</span>
                </div>
                """, unsafe_allow_html=True)

    update_progress(0)

    # Video display and results layout
    col_video, col_results = st.columns([0.55, 0.45])

    with col_video:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">📽️ Uploaded Video</div>
        </div>
        """, unsafe_allow_html=True)
        st.video(uploaded_file)

    with col_results:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">📊 Analysis Results</div>
        </div>
        """, unsafe_allow_html=True)

        results_placeholder = st.empty()

        # Processing with progress updates
        vid_path = None
        audio_wav_path = None
        analysis_successful = False

        try:
            # Step 1: Save uploaded video
            update_progress(1)
            time.sleep(0.5)

            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_vid_file:
                tmp_vid_file.write(uploaded_file.read())
                vid_path = tmp_vid_file.name

            # Step 2: Extract video features
            update_progress(2)
            time.sleep(0.5)

            video_feat_raw = extract_all_video_features(vid_path)
            if video_feat_raw is None:
                st.error("❌ Could not extract video features.")
                st.stop()
            video_feat_scaled = scaler_v.transform(video_feat_raw.reshape(1, -1))[0]

            # Step 3: Extract audio
            update_progress(3)
            time.sleep(0.5)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
                audio_wav_path = tmp_audio_file.name

            if not extract_audio(vid_path, audio_wav_path):
                st.error("❌ Could not extract audio from video.")
                st.stop()

            # Step 4: Transcribe audio
            update_progress(4)
            time.sleep(0.5)

            transcript = transcribe_audio(audio_wav_path)

            # Step 5: Extract features
            update_progress(5)
            time.sleep(0.5)

            mfcc_vec_raw = extract_mfcc_features(audio_wav_path)
            if mfcc_vec_raw is None:
                st.error("❌ Could not extract audio MFCC features.")
                st.stop()
            mfcc_vec_scaled = scaler_a.transform(mfcc_vec_raw.reshape(1, -1))[0]

            text_feat_scaled = np.zeros(768)
            if transcript:
                text_feat_raw = extract_text_features(transcript)
                if text_feat_raw is None:
                    st.warning("⚠️ Could extract transcript, but not text features. Using zero vector for text.")
                else:
                    text_feat_scaled = scaler_t.transform(text_feat_raw.reshape(1, -1))[0]
            else:
                st.warning("⚠️ Could not transcribe audio or transcript is empty. Using zero vector for text.")

            # Step 6: Run prediction
            update_progress(6)
            time.sleep(0.5)

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
            with results_placeholder.container():
                st.error(f"🚨 An error occurred during processing: {str(e)}")
                if st.checkbox("Show technical details"):
                    import traceback
                    st.code(traceback.format_exc())
        finally:
            # Cleanup temporary files
            if vid_path and os.path.exists(vid_path):
                os.remove(vid_path)
            if audio_wav_path and os.path.exists(audio_wav_path):
                os.remove(audio_wav_path)

        # Display results
        if analysis_successful:
            update_progress(6)  # Mark final step as completed

            with results_placeholder.container():
                # Sentiment result with enhanced styling
                sentiment_class = ""
                if sentiment == "Positive":
                    sentiment_class = "sentiment-positive"
                elif sentiment == "Negative":
                    sentiment_class = "sentiment-negative"
                else:
                    sentiment_class = "sentiment-neutral"

                st.markdown(f"""
                <div class="sentiment-result">
                    <div class="sentiment-badge {sentiment_class}">
                        {sentiment} Sentiment Detected
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Transcript section
                if transcript:
                    st.markdown("""
                    <div class="transcript-container">
                        <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">📝 Speech Transcript</h4>
                        <div class="transcript-text">
                    """, unsafe_allow_html=True)
                    st.markdown(f'"{transcript}"')
                    st.markdown("</div></div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="transcript-container">
                        <h4 style="color: #6b7280;">📝 Speech Transcript</h4>
                        <p style="color: #9ca3af; font-style: italic;">No transcript was available for text analysis.</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Confidence scores with visual bars
                st.markdown("""
                <div class="confidence-section">
                    <h4 style="color: #3b82f6; margin-bottom: 1rem;">🎯 Confidence Scores</h4>
                </div>
                """, unsafe_allow_html=True)

                for label, prob_val in prob_dict.items():
                    bar_class = ""
                    if label == "Positive":
                        bar_class = "confidence-fill-positive"
                    elif label == "Negative":
                        bar_class = "confidence-fill-negative"
                    else:
                        bar_class = "confidence-fill-neutral"

                    percentage = int(prob_val * 100)
                    st.markdown(f"""
                    <div class="confidence-bar">
                        <div class="confidence-label">{label}</div>
                        <div class="confidence-fill">
                            <div class="{bar_class}" style="width: {percentage}%; height: 100%; border-radius: 12px;">
                                <div class="confidence-value">{percentage}%</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Additional insights
                st.markdown("""
                <div style="margin-top: 2rem; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border-left: 3px solid #3b82f6;">
                    <h5 style="color: #3b82f6; margin-bottom: 0.5rem;">💡 Analysis Insights</h5>
                    <p style="color: #cbd5e1; margin: 0; font-size: 0.9rem;">
                        This analysis combines visual cues from facial expressions and body language,
                        acoustic features from speech patterns, and semantic understanding from transcribed content
                        to provide a comprehensive sentiment assessment.
                    </p>
                </div>
                """, unsafe_allow_html=True)

else:
    # Welcome message when no file is uploaded
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: rgba(59, 130, 246, 0.05); border-radius: 15px; margin: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎬</div>
        <h3 style="color: #3b82f6; margin-bottom: 1rem;">Ready to Analyze Sentiment</h3>
        <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Upload a video file above to get started. Our AI will analyze the visual, audio, and textual
            content to determine the sentiment expressed in your video.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">
        <strong>🎭 Multimodal Sentiment Analyzer</strong> | Built with TensorFlow, PyTorch & Streamlit<br>
        Created by Shashank | Powered by Advanced Multimodal AI Technology
    </div>
</div>
""", unsafe_allow_html=True)