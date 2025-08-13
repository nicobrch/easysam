from peewee import *
from .session import db


class BaseModel(Model):
    """Base model class that all models should inherit from"""
    class Meta:
        database = db


class Project(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=255)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


class VideoTypes(BaseModel):
    id = AutoField(primary_key=True)
    type = CharField(max_length=50, unique=True)


class Videos(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, backref='videos', on_delete='CASCADE')
    name = CharField(max_length=255)
    file_path = CharField(max_length=500)
    frame_directory = CharField(max_length=500)
    width = IntegerField()
    height = IntegerField()
    fps = FloatField()
    duration = FloatField()  # in seconds
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


class VideoInference(BaseModel):
    source_video = ForeignKeyField(
        Videos, backref='inference_source', on_delete='CASCADE')
    inference_video = ForeignKeyField(
        Videos, backref='inference_result', on_delete='CASCADE')
    model = CharField(max_length=255)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        primary_key = CompositeKey('source_video', 'inference_video')


class Object(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, backref='objects', on_delete='CASCADE')
    name = CharField(max_length=255)
    color = CharField(max_length=50)


class PointLabel(BaseModel):
    id = AutoField(primary_key=True)
    type = CharField(max_length=50, unique=True)


class ObjectPoint(BaseModel):
    id = AutoField(primary_key=True)
    object = ForeignKeyField(Object, backref='points', on_delete='CASCADE')
    video = ForeignKeyField(
        Videos, backref='object_points', on_delete='CASCADE')
    point_label = ForeignKeyField(
        PointLabel, backref='object_points', on_delete='CASCADE')
    x = IntegerField()
    y = IntegerField()
