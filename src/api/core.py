import logging
from typing import Optional, List, Tuple, Dict, Any
from .inference import InferenceAPI
from .db import DatabaseAPI

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

    def add_object_point(
        self,
        object_id: int,
        frame_idx: int,
        x: int,
        y: int,
        point_label_id: int,
        label: int = 1,
        clear_old_points: bool = False
    ) -> Tuple[Optional[Any], Optional[Tuple[int, List[int], List[Dict[str, Any]]]]]:
        """Create a new object point in the database and add it to the inference session.

        Args:
            object_id: Database ID of the object to add point for
            frame_idx: Frame index where the point is located
            x: X coordinate of the point
            y: Y coordinate of the point
            point_label_id: Database ID of the point label type
            label: Point label for inference (1 for positive, 0 for negative)
            clear_old_points: Whether to clear previous points in inference

        Returns:
            Tuple of (db_object_point, inference_result) where:
            - db_object_point: The created ObjectPoint database record or None if failed
            - inference_result: Tuple of (frame_index, object_ids, masks_rle) or None if failed

        Raises:
            RuntimeError: If no active inference session
        """
        # First, create the object point in the database
        db_object_point = self.db_api.create_object_point(
            object_id=object_id,
            video_id=self.video_id,
            point_label_id=point_label_id,
            x=x,
            y=y,
            frame_idx=frame_idx
        )

        if db_object_point is None:
            logger.error(
                f"Failed to create object point in database for object {object_id} "
                f"at frame {frame_idx}, coordinates ({x}, {y})"
            )
            return None, None

        logger.info(
            f"Created object point {db_object_point.id} in database for object {object_id} "
            f"at frame {frame_idx}, coordinates ({x}, {y})"
        )

        # Then, add the point to the inference session
        try:
            inference_result = self.inference_api.add_points(
                session_id=self.session_id,
                frame_index=frame_idx,
                object_id=object_id,
                points=[[x, y]],
                labels=[label],
                clear_old_points=clear_old_points
            )

            logger.info(
                f"Added point to inference session {self.session_id} for object {object_id} "
                f"at frame {frame_idx}, coordinates ({x}, {y})"
            )

            return db_object_point, inference_result

        except Exception as e:
            logger.error(
                f"Failed to add point to inference session {self.session_id}: {e}. "
                f"Database object point {db_object_point.id} was created but inference failed."
            )
            return db_object_point, None
