from typing import List, Optional, Dict, Any
from peewee import DoesNotExist, IntegrityError
from .session import get_db_session
from .models import (
    Project, VideoTypes, Videos, VideoInference,
    Object, PointLabel, ObjectPoint
)


class DatabaseAPI:
    """Database API class providing CRUD operations for all models"""

    # Project CRUD operations
    @staticmethod
    def create_project(name: str) -> Project:
        """Create a new project"""
        with get_db_session():
            return Project.create(name=name)

    @staticmethod
    def get_project(project_id: int) -> Optional[Project]:
        """Get a project by ID"""
        with get_db_session():
            try:
                return Project.get_by_id(project_id)
            except DoesNotExist:
                return None

    @staticmethod
    def get_all_projects() -> List[Project]:
        """Get all projects"""
        with get_db_session():
            return list(Project.select())

    @staticmethod
    def update_project(project_id: int, name: str) -> bool:
        """Update a project"""
        with get_db_session():
            try:
                project = Project.get_by_id(project_id)
                project.name = name
                project.save()
                return True
            except DoesNotExist:
                return False

    @staticmethod
    def delete_project(project_id: int) -> bool:
        """Delete a project"""
        with get_db_session():
            try:
                project = Project.get_by_id(project_id)
                project.delete_instance(recursive=True)
                return True
            except DoesNotExist:
                return False

    # VideoTypes CRUD operations
    @staticmethod
    def create_video_type(type_name: str) -> Optional[VideoTypes]:
        """Create a new video type"""
        with get_db_session():
            try:
                return VideoTypes.create(type=type_name)
            except IntegrityError:
                return None

    @staticmethod
    def get_video_type(type_id: int) -> Optional[VideoTypes]:
        """Get a video type by ID"""
        with get_db_session():
            try:
                return VideoTypes.get_by_id(type_id)
            except DoesNotExist:
                return None

    @staticmethod
    def get_all_video_types() -> List[VideoTypes]:
        """Get all video types"""
        with get_db_session():
            return list(VideoTypes.select())

    @staticmethod
    def delete_video_type(type_id: int) -> bool:
        """Delete a video type"""
        with get_db_session():
            try:
                video_type = VideoTypes.get_by_id(type_id)
                video_type.delete_instance()
                return True
            except DoesNotExist:
                return False

    # Videos CRUD operations
    @staticmethod
    def create_video(project_id: int, name: str, file_path: str, first_frame_path: str,
                     width: int, height: int, fps: float, duration: float) -> Optional[Videos]:
        """Create a new video"""
        with get_db_session():
            try:
                return Videos.create(
                    project=project_id,
                    name=name,
                    file_path=file_path,
                    first_frame_path=first_frame_path,
                    width=width,
                    height=height,
                    fps=fps,
                    duration=duration
                )
            except IntegrityError:
                return None

    @staticmethod
    def get_video(video_id: int) -> Optional[Videos]:
        """Get a video by ID"""
        with get_db_session():
            try:
                return Videos.get_by_id(video_id)
            except DoesNotExist:
                return None

    @staticmethod
    def get_videos_by_project(project_id: int) -> List[Videos]:
        """Get all videos for a project"""
        with get_db_session():
            return list(Videos.select().where(Videos.project == project_id))

    @staticmethod
    def get_all_videos() -> List[Videos]:
        """Get all videos"""
        with get_db_session():
            return list(Videos.select())

    @staticmethod
    def update_video(video_id: int, **kwargs) -> bool:
        """Update a video with provided fields"""
        with get_db_session():
            try:
                video = Videos.get_by_id(video_id)
                for key, value in kwargs.items():
                    if hasattr(video, key):
                        setattr(video, key, value)
                video.save()
                return True
            except DoesNotExist:
                return False

    @staticmethod
    def delete_video(video_id: int) -> bool:
        """Delete a video"""
        with get_db_session():
            try:
                video = Videos.get_by_id(video_id)
                video.delete_instance(recursive=True)
                return True
            except DoesNotExist:
                return False

    # VideoInference CRUD operations
    @staticmethod
    def create_video_inference(source_video_id: int, inference_video_id: int, model: str) -> Optional[VideoInference]:
        """Create a new video inference record"""
        with get_db_session():
            try:
                return VideoInference.create(
                    source_video=source_video_id,
                    inference_video=inference_video_id,
                    model=model
                )
            except IntegrityError:
                return None

    @staticmethod
    def get_video_inference(source_video_id: int, inference_video_id: int) -> Optional[VideoInference]:
        """Get a video inference record"""
        with get_db_session():
            try:
                return VideoInference.get(
                    VideoInference.source_video == source_video_id,
                    VideoInference.inference_video == inference_video_id
                )
            except DoesNotExist:
                return None

    @staticmethod
    def get_inferences_for_source(source_video_id: int) -> List[VideoInference]:
        """Get all inference records for a source video"""
        with get_db_session():
            return list(VideoInference.select().where(VideoInference.source_video == source_video_id))

    @staticmethod
    def delete_video_inference(source_video_id: int, inference_video_id: int) -> bool:
        """Delete a video inference record"""
        with get_db_session():
            try:
                inference = VideoInference.get(
                    VideoInference.source_video == source_video_id,
                    VideoInference.inference_video == inference_video_id
                )
                inference.delete_instance()
                return True
            except DoesNotExist:
                return False

    # Object CRUD operations
    @staticmethod
    def create_object(project_id: int, name: str, color: str) -> Optional[Object]:
        """Create a new object"""
        with get_db_session():
            try:
                return Object.create(project=project_id, name=name, color=color)
            except IntegrityError:
                return None

    @staticmethod
    def get_object(object_id: int) -> Optional[Object]:
        """Get an object by ID"""
        with get_db_session():
            try:
                return Object.get_by_id(object_id)
            except DoesNotExist:
                return None

    @staticmethod
    def get_objects_by_project(project_id: int) -> List[Object]:
        """Get all objects for a project"""
        with get_db_session():
            return list(Object.select().where(Object.project == project_id))

    @staticmethod
    def update_object(object_id: int, name: str = None, color: str = None) -> bool:
        """Update an object"""
        with get_db_session():
            try:
                obj = Object.get_by_id(object_id)
                if name is not None:
                    obj.name = name
                if color is not None:
                    obj.color = color
                obj.save()
                return True
            except DoesNotExist:
                return False

    @staticmethod
    def delete_object(object_id: int) -> bool:
        """Delete an object"""
        with get_db_session():
            try:
                obj = Object.get_by_id(object_id)
                obj.delete_instance(recursive=True)
                return True
            except DoesNotExist:
                return False

    # PointLabel CRUD operations
    @staticmethod
    def create_point_label(type_name: str) -> Optional[PointLabel]:
        """Create a new point label"""
        with get_db_session():
            try:
                return PointLabel.create(type=type_name)
            except IntegrityError:
                return None

    @staticmethod
    def get_point_label(label_id: int) -> Optional[PointLabel]:
        """Get a point label by ID"""
        with get_db_session():
            try:
                return PointLabel.get_by_id(label_id)
            except DoesNotExist:
                return None

    @staticmethod
    def get_all_point_labels() -> List[PointLabel]:
        """Get all point labels"""
        with get_db_session():
            return list(PointLabel.select())

    @staticmethod
    def delete_point_label(label_id: int) -> bool:
        """Delete a point label"""
        with get_db_session():
            try:
                label = PointLabel.get_by_id(label_id)
                label.delete_instance(recursive=True)
                return True
            except DoesNotExist:
                return False

    # ObjectPoint CRUD operations
    @staticmethod
    def create_object_point(object_id: int, video_id: int, point_label_id: int, x: int, y: int) -> Optional[ObjectPoint]:
        """Create a new object point"""
        with get_db_session():
            try:
                return ObjectPoint.create(
                    object=object_id,
                    video=video_id,
                    point_label=point_label_id,
                    x=x,
                    y=y
                )
            except IntegrityError:
                return None

    @staticmethod
    def get_object_point(point_id: int) -> Optional[ObjectPoint]:
        """Get an object point by ID"""
        with get_db_session():
            try:
                return ObjectPoint.get_by_id(point_id)
            except DoesNotExist:
                return None

    @staticmethod
    def get_object_points_by_object(object_id: int) -> List[ObjectPoint]:
        """Get all points for an object"""
        with get_db_session():
            return list(ObjectPoint.select().where(ObjectPoint.object == object_id))

    @staticmethod
    def get_object_points_by_video(video_id: int) -> List[ObjectPoint]:
        """Get all object points for a video"""
        with get_db_session():
            return list(ObjectPoint.select().where(ObjectPoint.video == video_id))

    @staticmethod
    def update_object_point(point_id: int, x: int = None, y: int = None) -> bool:
        """Update an object point coordinates"""
        with get_db_session():
            try:
                point = ObjectPoint.get_by_id(point_id)
                if x is not None:
                    point.x = x
                if y is not None:
                    point.y = y
                point.save()
                return True
            except DoesNotExist:
                return False

    @staticmethod
    def delete_object_point(point_id: int) -> bool:
        """Delete an object point"""
        with get_db_session():
            try:
                point = ObjectPoint.get_by_id(point_id)
                point.delete_instance()
                return True
            except DoesNotExist:
                return False

    # Utility methods
    @staticmethod
    def initialize_database():
        """Initialize the database by creating all tables"""
        from .models import Project, VideoTypes, Videos, VideoInference, Object, PointLabel, ObjectPoint
        with get_db_session() as db:
            db.create_tables([
                Project, VideoTypes, Videos, VideoInference,
                Object, PointLabel, ObjectPoint
            ], safe=True)

    @staticmethod
    def get_project_summary(project_id: int) -> Optional[Dict[str, Any]]:
        """Get a summary of a project including counts of related objects"""
        with get_db_session():
            try:
                project = Project.get_by_id(project_id)
                videos_count = Videos.select().where(Videos.project == project_id).count()
                objects_count = Object.select().where(Object.project == project_id).count()

                return {
                    'project': project,
                    'videos_count': videos_count,
                    'objects_count': objects_count
                }
            except DoesNotExist:
                return None


# Create a singleton instance for easy access
db_api = DatabaseAPI()
