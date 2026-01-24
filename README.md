# Multimodal Sentiment Classifier

## 🎬 Project Overview

This project implements a Multimodal Sentiment Classifier that analyzes short video clips (5-15 seconds) to predict sentiment as **Positive**, **Negative**, or **Neutral**. It leverages three distinct modalities:
* **Video:** Visual features extracted from video frames.
* **Audio:** Acoustic features (MFCCs) extracted from the audio track.
* **Text:** Semantic features extracted from the transcribed speech content.

The primary goal was to build an end-to-end pipeline, from raw video input to sentiment prediction, and demonstrate its functionality through a user-friendly Streamlit application.

## ✨ Features

* Processes video, audio, and text modalities for sentiment analysis.
* Uses ResNet18 for video features, MFCCs for audio features, and DistilBERT for text embeddings.
* Employs an early fusion mechanism to combine multimodal features.
* Trained on a subset of the CMU-MOSI mini dataset.
* Includes a Streamlit web application for uploading video clips and receiving real-time sentiment predictions.

## 📂 Project Structure
```
├── app/
│   └── app.py                      # Streamlit application script
├── data/
│   ├── mini_dataset/               # (Optional) Raw data (audio, video, transcripts)
│   │   ├── segmented_audio/
│   │   ├── segmented_video/
│   │   └── segmented_transcripts/
│   ├── mini_audio_features.pkl     # Pre-extracted audio features
│   ├── mini_video_features.pkl     # Pre-extracted video features
│   ├── mini_text_features.pkl      # Pre-extracted text features
│   └── processed_dataset.csv       # CSV linking clips to annotations
├── models/
│   ├── final_multimodal_logits_model.h5 # Trained fusion model
│   ├── label_encoder.pkl           # Saved LabelEncoder
│   ├── scaler_audio.pkl            # Saved StandardScaler for audio
│   ├── scaler_video.pkl            # Saved StandardScaler for video
│   ├── scaler_text.pkl             # Saved StandardScaler for text
│   └── multimodal_model.py         # Training script for the fusion model
├── preprocessing/
│   ├── extract_audio.py            # Extracts audio from video
│   ├── extract_frames.py           # Extracts frames from video (if used by video feature extractor)
│   ├── extract_all_audio_features.py # Generates MFCC features
│   ├── extract_all_video_features.py # Generates ResNet18 video features
│   ├── extract_all_text_features.py  # Generates DistilBERT text features (mean-pooled)
│   └── transcribe_audio.py         # Transcribes audio to text
├── README.md                       # This file
├── requirements.txt                # Python package dependencies
└── Report.pdf                      # (Example name for your final project report)
```
## Setup Instructions

### Prerequisites

* Python (3.8 - 3.10 recommended)
* `pip` (Python package installer)
* **FFMPEG:** MoviePy (used for audio/video processing) requires FFMPEG to be installed on your system and accessible in your PATH.
    * **Windows:** Download FFMPEG static builds, extract, and add the `bin` folder to your system's PATH environment variable.
    * **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg`
    * **macOS:** `brew install ffmpeg`

### Installation

1.  **Clone the repository (or download and extract the project files):**
    ```bash
    # If using Git
    # git clone [your-repo-link]
    # cd [your-repo-name]
    ```
    Navigate to the project's root directory.

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv multimodal_env
    ```
    Activate the environment:
    * Windows (Command Prompt/PowerShell):
        ```cmd
        multimodal_env\Scripts\activate
        ```
    * macOS/Linux (Bash/Zsh):
        ```bash
        source multimodal_env/bin/activate
        ```

3.  **Install dependencies:**
    Ensure your virtual environment is activated, then run:
    ```bash
    pip install -r requirements.txt
    ```

### Dataset & Pre-trained Models

* This project assumes pre-extracted features (`mini_audio_features.pkl`, `mini_video_features.pkl`, `mini_text_features.pkl`), the dataset metadata (`processed_dataset.csv`), the trained Keras model (`final_multimodal_logits_model.h5`), and scikit-learn scalers/encoder (`*.pkl`) are present in the `data/` and `models/` directories respectively as per the structure above.
* These files are necessary to directly run the Streamlit application or re-evaluate the model.

## 🚀 Running the Code

Ensure your virtual environment (`multimodal_env`) is activated before running any scripts.

### 1. Feature Extraction (Optional - If Re-generating Features)

The required `.pkl` feature files are expected to be provided. If you need to re-generate them from raw segmented video/audio/text:
* Populate the `data/mini_dataset/segmented_audio/`, `data/mini_dataset/segmented_video/`, and `data/mini_dataset/segmented_transcripts/` directories with the respective data.
* Run the corresponding scripts:
    ```bash
    python preprocessing/extract_all_audio_features.py
    python preprocessing/extract_all_video_features.py
    python preprocessing/extract_all_text_features.py
    ```
    *Note: Ensure the input/output path constants within these scripts are correctly set if you modify the directory structure.*

### 2. Model Training (Optional - If Re-training the Model)

To re-train the multimodal fusion model using the `.pkl` feature files:
```bash
python models/multimodal_model.py
```
This script will:

Load the pre-extracted features.
Train the model.
Save the trained model (final_multimodal_logits_model.h5), label encoder (label_encoder.pkl), and feature scalers (scaler_*.pkl) to the models/ directory.
3. Running the Streamlit Application
To launch the interactive sentiment prediction web application:

```bash
streamlit run app/app.py --server.fileWatcherType none
```
This will start a local server and typically open the application in your default web browser (e.g., at http://localhost:8501). You can then upload a video clip to get its sentiment analyzed.

📄 Key Files Explained
* **app/app.py:** The main script for the Streamlit web application. Handles video upload, calls preprocessing functions, loads the trained model and scalers, performs prediction, and displays results.
* **models/multimodal_model.py:** The script used to define, train, and evaluate the multimodal fusion model. It also saves the trained model, label encoder, and feature scalers.
* **preprocessing/:** This directory contains scripts for:
* **extract_audio.py:** Extracting audio from video files.
* **transcribe_audio.py:** Converting speech in audio files to text.
* **extract_all_audio_features.py:** Computing MFCC features from audio.
* **extract_all_video_features.py:** Computing ResNet18 features from video frames.
* **extract_all_text_features.py:** Computing DistilBERT embeddings from text.
* **requirements.txt:** Lists all Python dependencies required for the project.
* **models/*.h5, models/*.pkl:** Stored trained Keras model, scikit-learn label encoder, and scalers.
* **data/*.pkl, data/*.csv:** Stored pre-extracted features and dataset metadata.
📈 Results Summary
The model was trained on a subset of 400 clips from the CMU-MOSI mini dataset and achieved a test accuracy of 76.25%.

Key F1-Scores on the test set:

* Positive Class: 0.83
* Negative Class: 0.71
* Neutral Class: 0.44
  
