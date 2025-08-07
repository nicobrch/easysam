from peewee import *

# Define the database
DATABASE_PATH = 'easysam.db'
db = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    """Base model class that all models should inherit from"""
    class Meta:
        database = db


def get_db():
    """Get a database connection. Use this in other parts of the app."""
    if db.is_closed():
        db.connect()
    return db


def get_db_session():
    """Context manager for database sessions. Automatically handles connection lifecycle."""
    class DatabaseSession:
        def __enter__(self):
            if db.is_closed():
                db.connect()
            return db

        def __exit__(self, exc_type, exc_val, exc_tb):
            if not db.is_closed():
                db.close()

    return DatabaseSession()


def close_db():
    """Close the database connection if it's open."""
    if not db.is_closed():
        db.close()
        db.close()
