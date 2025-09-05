from pathlib import Path

# Define the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = SRC_DIR / "assets"
UPLOADS_DIR = ASSETS_DIR / "uploads"


# Resolve paths to specific asset types using video names
def get_original_frames_path(video_name: str) -> Path:
    return UPLOADS_DIR / video_name / "original_frames"


def get_processed_frames_path(video_name: str) -> Path:
    return UPLOADS_DIR / video_name / "processed_frames"


def get_detection_labels_path(video_name: str) -> Path:
    return UPLOADS_DIR / video_name / "detection_labels"


def get_segmentation_labels_path(video_name: str) -> Path:
    return UPLOADS_DIR / video_name / "segmentation_labels"


def get_dataset_path(video_name: str) -> Path:
    return UPLOADS_DIR / video_name / "dataset"
