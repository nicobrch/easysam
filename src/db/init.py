import os
from .session import db
from .models import (
    Project, VideoTypes, Videos, VideoInference,
    Object, PointLabel, ObjectPoint
)


def initialize_database():
    """Initialize the database, create tables, and seed initial data"""
    try:
        # Connect to the database
        db.connect()

        # Create all tables if they don't exist
        db.create_tables([
            Project, VideoTypes, Videos, VideoInference,
            Object, PointLabel, ObjectPoint
        ], safe=True)

        # Seed initial data
        seed_data()

        print(
            f"Database initialized successfully at: {os.path.abspath('easysam.db')}")

    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        # Close the connection
        if not db.is_closed():
            db.close()


def seed_data():
    """Seed the database with initial data"""
    # Seed VideoTypes
    video_types = ["source", "inference"]
    for video_type in video_types:
        VideoTypes.get_or_create(type=video_type)

    # Seed PointLabel
    point_labels = ["positive", "negative"]
    for label_type in point_labels:
        PointLabel.get_or_create(type=label_type)


if __name__ == "__main__":
    initialize_database()
