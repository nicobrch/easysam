import logging
from typing import Optional
from .inference import InferenceAPI
from ..db.api import DatabaseAPI

logger = logging.getLogger(__name__)


class CoreAPI:
    """Core API class that integrates inference capabilities with database operations"""

    def __init__(self, video_id: int, model_size: str = "base_plus"):
        """Initialize CoreAPI with a video and model configuration.

        Args:
            video_id: Database ID of the video to work with
            model_size: SAM2 model size ("tiny", "small", "base_plus", "large")

        Raises:
            ValueError: If video not found in database
            RuntimeError: If failed to start inference session
        """
        self.video_id = video_id
        self.model_size = model_size

        # Initialize database API
        self.db_api = DatabaseAPI()

        # Get video information from database
        self.video = self.db_api.get_video(video_id)
        if self.video is None:
            raise ValueError(f"Video with ID {video_id} not found in database")

        # Initialize inference API
        self.inference_api = InferenceAPI(model_size)

        # Start inference session with video frames
        frame_directory = self._get_frame_directory()

        try:
            self.session_id = self.inference_api.start_session(frame_directory)
            logger.info(
                f"Started CoreAPI session {self.session_id} for video {video_id}")
        except Exception as e:
            logger.error(
                f"Failed to start inference session for video {video_id}: {e}")
            raise RuntimeError(f"Failed to initialize inference session: {e}")

    def _get_frame_directory(self) -> str:
        """Get the frame directory path for the video.

        Returns:
            str: Path to the directory containing video frames
        """
        return self.video.frame_directory

    def close(self):
        """Close the inference session and clean up resources."""
        if hasattr(self, 'session_id'):
            success = self.inference_api.close_session(self.session_id)
            if success:
                logger.info(f"Closed CoreAPI session {self.session_id}")
            else:
                logger.warning(f"Failed to close session {self.session_id}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically close session."""
        self.close()
