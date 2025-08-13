import os
import cv2
import supervision as sv
from typing import Optional


def extract_frames(
    video_path: str,
    output_dir: str,
    frame_step: int = 1,
    start_frame: int = 0,
    end_frame: Optional[int] = None
) -> None:
    """
    Extract frames from a video at specified intervals using supervision.

    Args:
        video_path: Path to the input video file
        output_dir: Directory where extracted frames will be saved
        frame_step: Interval between extracted frames (stride)
        start_frame: Starting frame position
        end_frame: Ending frame position (None for entire video)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get video frames generator with specified stride
    frames_generator = sv.get_video_frames_generator(
        source_path=video_path,
        stride=frame_step,
        start=start_frame,
        end=end_frame
    )

    # Extract and save frames
    for frame_idx, frame in enumerate(frames_generator):
        # Create filename with zero-padded frame number
        frame_filename = f"frame_{frame_idx:06d}.jpg"
        frame_path = os.path.join(output_dir, frame_filename)

        # Save frame as image
        cv2.imwrite(frame_path, frame)

    print(f"Extracted frames saved to: {output_dir}")
