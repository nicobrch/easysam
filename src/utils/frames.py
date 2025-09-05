import subprocess
from pathlib import Path
from typing import List, Union


def extract_frames(video_path: Union[str, Path], output_dir: Union[str, Path], frame_step: int) -> List[Path]:
    """
    Extract PNG frames from a video using ffmpeg with CUDA hardware acceleration.

    - Frames are saved with 6-digit padding using the original video file name:
      e.g., "<video-stem>_000001.png"
    - frame_step keeps 1 frame every N frames (1=every frame, 2=every other frame, etc.).

    Args:
        video_path: Path to the input video file.
        output_dir: Directory where extracted frames will be saved (created if missing).
        frame_step: Keep one frame every `frame_step` frames. Must be >= 1.

    Returns:
        A sorted list of Paths to the extracted frames.

    Raises:
        ValueError: If frame_step < 1.
        RuntimeError: If ffmpeg is not found or the command fails.
    """
    if frame_step < 1:
        raise ValueError("frame_step must be >= 1")

    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = video_path.stem
    output_pattern = output_dir / f"{base_name}_%06d.png"

    # Use select filter to keep one frame every `frame_step` frames.
    # Escape comma in the expression for ffmpeg filter syntax.
    filter_expr = f"select=not(mod(n\\,{frame_step}))"

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-nostdin",
        "-y",
        "-hwaccel",
        "cuda",
        "-i",
        str(video_path),
        "-vf",
        filter_expr,
        "-vsync",
        "vfr",
        "-start_number",
        "1",
        str(output_pattern),
    ]

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError as e:
        raise RuntimeError(
            "ffmpeg not found. Ensure ffmpeg is installed and in PATH.") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"ffmpeg failed with exit code {e.returncode}") from e

    # Collect and return extracted frame paths
    return sorted(output_dir.glob(f"{base_name}_*.png"))
