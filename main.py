import pickle

with open('data\mini_dataset\mini_audio_features.pkl', 'rb') as f:
    audio = pickle.load(f)
    print("Audio keys:", list(audio.keys())[:3])
    
with open('data\mini_dataset\mini_video_features.pkl', 'rb') as f:
    audio = pickle.load(f)
    print("Video keys:", list(audio.keys())[:3])
    
with open('data\mini_dataset\mini_text_features.pkl', 'rb') as f:
    audio = pickle.load(f)
    print("Text keys:", list(audio.keys())[:3])
    
    
    
import pandas as pd

df = pd.read_csv('data/processed_dataset.csv')
print(df[['clip_id', 'annotation']].head(3))
import pandas as pd
print(df['annotation'].value_counts())


