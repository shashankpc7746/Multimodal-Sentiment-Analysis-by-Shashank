import os
import librosa
import numpy as np
import pickle
from tqdm import tqdm

# Path to segmented audio folder and output location
AUDIO_FOLDER = 'data/mini_dataset/segmented_audio'
OUTPUT_PATH = 'data/mini_dataset/mini_audio_features.pkl'

# Parameters for MFCC
SAMPLE_RATE = 16000
N_MFCC = 13

def extract_mfcc_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
        mfcc_mean = np.mean(mfcc.T, axis=0)  # Take average across time
        return mfcc_mean
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None

def main():
    feature_dict = {}

    print("Extracting MFCC features from all segmented audio clips...\n")

    for filename in tqdm(os.listdir(AUDIO_FOLDER)):
        if filename.endswith('.wav'):
            clip_id = filename.replace('.wav', '')  # e.g., '_dI--eQ6qVU_1'
            file_path = os.path.join(AUDIO_FOLDER, filename)
            mfcc = extract_mfcc_features(file_path)
            if mfcc is not None:
                feature_dict[clip_id] = mfcc

    # Save to .pkl
    with open(OUTPUT_PATH, 'wb') as f:
        pickle.dump(feature_dict, f)

    print(f"\n✅ Extracted MFCC features for {len(feature_dict)} audio clips.")
    print(f"🔸 Saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()