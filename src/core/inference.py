import contextlib
import logging
import os
import uuid
from threading import Lock
from typing import Any, Dict, List, Tuple

import numpy as np
import torch
from sam2.build_sam import build_sam2_video_predictor
from pycocotools.mask import encode as encode_masks


logger = logging.getLogger(__name__)


class InferenceAPI:

    def __init__(self, model_size: str) -> None:
        super(InferenceAPI, self).__init__()

        self.session_states: Dict[str, Any] = {}
        self.score_thresh = 0

        if model_size == "tiny":
            checkpoint = "checkpoints/sam2.1_hiera_tiny.pt"
            model_cfg = "config/sam2.1_hiera_t.yaml"
        elif model_size == "small":
            checkpoint = "checkpoints/sam2.1_hiera_small.pt"
            model_cfg = "config/sam2.1_hiera_s.yaml"
        elif model_size == "large":
            checkpoint = "checkpoints/sam2.1_hiera_large.pt"
            model_cfg = "config/sam2.1_hiera_l.yaml"
        else:  # base_plus (default)
            checkpoint = "checkpoints/sam2.1_hiera_base_plus.pt"
            model_cfg = "config/sam2.1_hiera_b+.yaml"

        # select the device for computation
        force_cpu_device = os.environ.get(
            "SAM2_DEMO_FORCE_CPU_DEVICE", "0") == "1"
        if force_cpu_device:
            logger.info("forcing CPU device for SAM 2 demo")
        if torch.cuda.is_available() and not force_cpu_device:
            device = torch.device("cuda")
        elif torch.backends.mps.is_available() and not force_cpu_device:
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
        logger.info(f"using device: {device}")

        if device.type == "cuda":
            # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
            if torch.cuda.get_device_properties(0).major >= 8:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
        elif device.type == "mps":
            logging.warning(
                "\nSupport for MPS devices is preliminary. SAM 2 is trained with CUDA and might "
                "give numerically different outputs and sometimes degraded performance on MPS. "
                "See e.g. https://github.com/pytorch/pytorch/issues/84936 for a discussion."
            )

        self.device = device
        self.predictor = build_sam2_video_predictor(
            model_cfg, checkpoint, device=device
        )
        self.inference_lock = Lock()

    def autocast_context(self):
        if self.device.type == "cuda":
            return torch.autocast("cuda", dtype=torch.bfloat16)
        else:
            return contextlib.nullcontext()

    def start_session(self, frame_directory: str) -> str:
        """Start a new inference session for a video file using it's frame directory.

        Args:
            frame_directory: Path to the directory containing video frames

        Returns:
            session_id: Unique identifier for the session
        """
        with self.autocast_context(), self.inference_lock:
            session_id = str(uuid.uuid4())
            # for MPS devices, we offload the video frames to CPU by default to avoid
            # memory fragmentation in MPS (which sometimes crashes the entire process)
            offload_video_to_cpu = self.device.type == "mps"
            inference_state = self.predictor.init_state(
                frame_directory,
                offload_video_to_cpu=offload_video_to_cpu,
            )
            self.session_states[session_id] = {
                "canceled": False,
                "state": inference_state,
            }
            logger.info(
                f"Started new session {session_id} for video frames: {frame_directory}")
            return session_id

    def close_session(self, session_id: str) -> bool:
        """Close an inference session and clean up resources.

        Args:
            session_id: The session identifier to close

        Returns:
            bool: True if session was successfully closed, False if session not found
        """
        return self.__clear_session_state(session_id)

    def __clear_session_state(self, session_id: str) -> bool:
        session = self.session_states.pop(session_id, None)
        if session is None:
            logger.warning(
                f"cannot close session {session_id} as it does not exist (it might have expired); "
                f"{self.__get_session_stats()}"
            )
            return False
        else:
            logger.info(
                f"removed session {session_id}; {self.__get_session_stats()}")
            return True

    def __get_session(self, session_id: str):
        session = self.session_states.get(session_id, None)
        if session is None:
            raise RuntimeError(
                f"Cannot find session {session_id}; it might have expired"
            )
        return session

    def __get_session_stats(self):
        """Get a statistics string for live sessions and their GPU usage."""
        # print both the session ids and their video frame numbers
        live_session_strs = [
            f"'{session_id}' ({session['state']['num_frames']} frames, "
            f"{len(session['state']['obj_ids'])} objects)"
            for session_id, session in self.session_states.items()
        ]

        if torch.cuda.is_available():
            gpu_stats = (
                f"GPU memory: "
                f"{torch.cuda.memory_allocated() // 1024**2} MiB used and "
                f"{torch.cuda.memory_reserved() // 1024**2} MiB reserved"
                f" (max over time: {torch.cuda.max_memory_allocated() // 1024**2} MiB used "
                f"and {torch.cuda.max_memory_reserved() // 1024**2} MiB reserved)"
            )
        else:
            gpu_stats = "GPU not available"

        session_stats_str = (
            f"live sessions: [{', '.join(live_session_strs)}], {gpu_stats}"
        )
        return session_stats_str

    def add_points(
        self,
        session_id: str,
        frame_index: int,
        object_id: int,
        points: List[List[float]],
        labels: List[int],
        clear_old_points: bool = True
    ) -> Tuple[int, List[int], List[Dict[str, Any]]]:
        """Add new points on a specific video frame.

        Args:
            session_id: The session identifier
            frame_index: Frame index to add points to
            object_id: Object ID to track
            points: List of [x, y] coordinates
            labels: List of labels (1 for positive, 0 for negative)
            clear_old_points: Whether to clear previous points

        Returns:
            Tuple of (frame_index, object_ids, masks_rle)
        """
        with self.autocast_context(), self.inference_lock:
            session = self.__get_session(session_id)
            inference_state = session["state"]

            # add new prompts and instantly get the output on the same frame
            frame_idx, object_ids, masks = self.predictor.add_new_points_or_box(
                inference_state=inference_state,
                frame_idx=frame_index,
                obj_id=object_id,
                points=points,
                labels=labels,
                clear_old_points=clear_old_points,
                normalize_coords=False,
            )

            masks_binary = (masks > self.score_thresh)[:, 0].cpu().numpy()

            # Use the existing helper method
            masks_rle = self.__get_rle_mask_list(
                object_ids=object_ids, masks=masks_binary
            )

            return frame_idx, object_ids, masks_rle

    def __get_rle_mask_list(
        self, object_ids: List[int], masks: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Return a list of mask data for objects."""
        masks_rle = []
        for obj_id, mask in zip(object_ids, masks):
            mask_rle = encode_masks(np.array(mask, dtype=np.uint8, order="F"))
            mask_rle["counts"] = mask_rle["counts"].decode()
            masks_rle.append({
                "object_id": obj_id,
                "mask": {
                    "size": mask_rle["size"],
                    "counts": mask_rle["counts"]
                }
            })
        return masks_rle

    def __get_mask_for_object(
        self, object_id: int, mask: np.ndarray
    ) -> Dict[str, Any]:
        """Create mask data for an object."""
        mask_rle = encode_masks(np.array(mask, dtype=np.uint8, order="F"))
        mask_rle["counts"] = mask_rle["counts"].decode()
        return {
            "object_id": object_id,
            "mask": {
                "size": mask_rle["size"],
                "counts": mask_rle["counts"]
            }
        }

    def clear_points_in_frame(
        self,
        session_id: str,
        frame_index: int,
        object_id: int
    ) -> Tuple[int, List[int], List[Dict[str, Any]]]:
        """Remove all input points in a specific frame.

        Args:
            session_id: The session identifier
            frame_index: Frame index to clear points from
            object_id: Object ID to clear points for

        Returns:
            Tuple of (frame_index, object_ids, masks_rle)
        """
        with self.autocast_context(), self.inference_lock:
            session = self.__get_session(session_id)
            inference_state = session["state"]

            frame_idx, obj_ids, video_res_masks = (
                self.predictor.clear_all_prompts_in_frame(
                    inference_state, frame_index, object_id
                )
            )
            masks_binary = (video_res_masks > self.score_thresh)[
                :, 0].cpu().numpy()

            masks_rle = self.__get_rle_mask_list(
                object_ids=obj_ids, masks=masks_binary
            )

            return frame_idx, obj_ids, masks_rle

    def clear_points_in_video(self, session_id: str) -> bool:
        """Remove all input points in all frames throughout the video.

        Args:
            session_id: The session identifier

        Returns:
            bool: True if successful
        """
        with self.autocast_context(), self.inference_lock:
            session = self.__get_session(session_id)
            inference_state = session["state"]
            self.predictor.reset_state(inference_state)
            return True

    def remove_object(
        self,
        session_id: str,
        object_id: int
    ) -> List[Tuple[int, List[int], List[Dict[str, Any]]]]:
        """Remove an object id from the tracking state.

        Args:
            session_id: The session identifier
            object_id: Object ID to remove from tracking

        Returns:
            List of tuples containing (frame_index, object_ids, masks_rle) for updated frames
        """
        with self.autocast_context(), self.inference_lock:
            session = self.__get_session(session_id)
            inference_state = session["state"]
            new_obj_ids, updated_frames = self.predictor.remove_object(
                inference_state, object_id
            )

            results = []
            for frame_index, video_res_masks in updated_frames:
                masks = (video_res_masks > self.score_thresh)[
                    :, 0].cpu().numpy()
                rle_mask_list = self.__get_rle_mask_list(
                    object_ids=new_obj_ids, masks=masks
                )
                results.append((frame_index, new_obj_ids, rle_mask_list))

            return results
