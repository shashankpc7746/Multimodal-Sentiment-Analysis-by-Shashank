# extract_mfcc.py

import librosa
import numpy as np
import os

def extract_mfcc_features(audio_path, output_path, n_mfcc=13):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        np.save(output_path, mfcc)
        print(f"MFCC features saved at: {output_path}")
    except Exception as e:
        print("Error extracting MFCC:", e)

if __name__ == "__main__":
    # Example usage
    audio_path = "data/processed_audio/sample_audio.wav"
    mfcc_output_path = "data/processed_audio/sample_mfcc.npy"

    extract_mfcc_features(audio_path, mfcc_output_path)
