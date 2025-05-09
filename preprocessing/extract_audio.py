# preprocessing/extract_audio.py
from moviepy.editor import VideoFileClip
import os
import traceback # For more detailed error printing

def extract_audio(video_input_path, audio_output_path):
    """
    Extracts audio from a video file and saves it.
    Returns True on success, False on failure.
    """
    try:
        # --- Create the output directory if it doesn't exist ---
        output_dir = os.path.dirname(audio_output_path)
        if output_dir and not os.path.exists(output_dir): # Check if output_dir is not empty
            print(f"Creating directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        # --- End of directory creation ---

        if not os.path.exists(video_input_path):
            print(f"Error: Video input file not found at '{video_input_path}'")
            return False

        print(f"Extracting audio from '{video_input_path}' to '{audio_output_path}'")
        video_clip = VideoFileClip(video_input_path)
        
        if video_clip.audio is None:
            print(f"Error: No audio track found in video '{video_input_path}'.")
            video_clip.close()
            return False
            
        # Use logger=None to prevent FFMPEG from printing to stdout/stderr directly
        # unless you are debugging FFMPEG itself.
        video_clip.audio.write_audiofile(audio_output_path, logger=None) 
        
        video_clip.close() # Release resources explicitly
        if hasattr(video_clip, 'reader') and video_clip.reader: video_clip.reader.close()
        if hasattr(video_clip, 'audio') and hasattr(video_clip.audio, 'reader') and video_clip.audio.reader: video_clip.audio.reader.close_proc()


        print(f"Audio successfully extracted to '{audio_output_path}'")
        return True

    except Exception as e:
        print(f"Error during audio extraction for {video_input_path}: {e}")
        print(traceback.format_exc()) # Print full traceback for the exception
        # Try to close resources even if an error occurred
        if 'video_clip' in locals():
            video_clip.close()
            if hasattr(video_clip, 'reader') and video_clip.reader: video_clip.reader.close()
            if hasattr(video_clip, 'audio') and hasattr(video_clip.audio, 'reader') and video_clip.audio.reader: video_clip.audio.reader.close_proc()
        return False

# --- Guard any direct execution / test code ---
# If line 24 in your original file was part of a direct test call,
# it should be moved into this block.
if __name__ == '__main__':
    print("Running extract_audio.py as a script (for testing purposes).")
    
    # Example: Define paths for a test case
    # You should have a sample video in 'data/test_videos/' for this test to run.
    test_video_input_dir = "data/raw_video_clips" # Make sure this directory exists for testing
    test_video_filename = "sample_video.mp4" # Put a sample video here
    test_video_path = os.path.join(test_video_input_dir, test_video_filename)

    test_audio_output_dir = "data/processed_audio" # Test output directory
    test_audio_filename = "sample_audio.wav"
    test_audio_output_path = os.path.join(test_audio_output_dir, test_audio_filename)

    # Create test video directory if it doesn't exist for the example
    if not os.path.exists(test_video_input_dir):
        os.makedirs(test_video_input_dir)
        print(f"Created test directory {test_video_input_dir}. Please add {test_video_filename} for testing.")

    if os.path.exists(test_video_path):
        print(f"\n--- Test: Attempting to extract audio from '{test_video_path}' ---")
        if extract_audio(test_video_path, test_audio_output_path):
            print("--- Test: Audio extraction successful ---")
        else:
            print("--- Test: Audio extraction failed ---")
    else:
        print(f"\n--- Test: Skipping test, video file '{test_video_path}' not found. ---")