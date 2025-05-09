import speech_recognition as sr

def transcribe_audio(audio_path):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    try:
        # Load the audio file
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)  # Record the entire audio file
        
        # Recognize the speech in the audio
        transcript = recognizer.recognize_google(audio)
        print("Transcript:", transcript)
        return transcript
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

if __name__ == "__main__":
    audio_path = "data/processed_audio/sample_audio.wav"  # Update with your audio file path
    transcript = transcribe_audio(audio_path)
    
    if transcript:
        with open("data/transcripts/sample_transcript.txt", "w") as f:
            f.write(transcript)
        print("Transcript saved to data/transcripts/sample_transcript.txt")
