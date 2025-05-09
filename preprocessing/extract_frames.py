import os
from moviepy.editor import VideoFileClip
from PIL import Image  # Add this import

def extract_frames(video_path, output_folder, frame_rate=1):
    """
    Extract frames from the video at a given frame rate.
    
    :param video_path: Path to the input video file.
    :param output_folder: Folder where the extracted frames will be saved.
    :param frame_rate: Rate at which to extract frames (frames per second).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the video clip
    video = VideoFileClip(video_path)

    # Extract frames at the specified frame rate
    for i, frame in enumerate(video.iter_frames(fps=frame_rate, dtype='uint8')):
        frame_filename = os.path.join(output_folder, f"frame_{i:04d}.jpg")
        image = Image.fromarray(frame)  # Convert NumPy array to image
        image.save(frame_filename, format='JPEG')  # Save as JPEG

    print(f"Frames extracted successfully. Total frames: {i + 1}")

# Example usage:
video_path = "data/raw_video_clips/sample_video.mp4"
output_folder = "data/processed_frames"
extract_frames(video_path, output_folder)
