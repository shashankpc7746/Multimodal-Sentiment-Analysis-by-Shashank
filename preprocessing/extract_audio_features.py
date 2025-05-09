import os
import librosa
import numpy as np
import pickle

def extract_mfcc_features(audio_path, n_mfcc=40):
    y, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfcc.T, axis=0)  # Shape: (n_mfcc,)

def extract_audio_features(audio_folder, output_file="data/audio_features.pkl"):
    audio_features = {}

    for filename in os.listdir(audio_folder):
        if filename.endswith(".wav"):
            path = os.path.join(audio_folder, filename)
            print(f"Extracting from {filename}")
            mfcc = extract_mfcc_features(path)
            audio_features[filename] = mfcc  # Directly save as NumPy array

    with open(output_file, "wb") as f:
        pickle.dump(audio_features, f)

    print(f"Saved all features to {output_file}")

# Example usage
extract_audio_features("data/processed_audio")
