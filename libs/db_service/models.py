import os
import datetime
from peewee import SqliteDatabase, Model, CharField, TextField, DateTimeField, BooleanField, ForeignKeyField, PostgresqlDatabase
from playhouse.db_url import connect

# Database setup
# Use an environment variable for the database path, defaulting to local sqlite
DB_URL = os.getenv("DATABASE_URL", "sqlite:///thoughts.db")
db = connect(DB_URL)

class BaseModel(Model):
    class Meta:
        database = db

class Thought(BaseModel):
    title = CharField()
    content = TextField()
    status = CharField(default="pending")  # pending, processed, error
    is_generated = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Thought, self).save(*args, **kwargs)

class Tag(BaseModel):
    name = CharField(unique=True)

class ThoughtTag(BaseModel):
    thought = ForeignKeyField(Thought, backref='tags')
    tag = ForeignKeyField(Tag, backref='thoughts')
    is_generated = BooleanField(default=False)

class Emotion(BaseModel):
    name = CharField(unique=True)

class ThoughtEmotion(BaseModel):
    thought = ForeignKeyField(Thought, backref='emotions')
    emotion = ForeignKeyField(Emotion, backref='thoughts')
    is_generated = BooleanField(default=False)

class ThoughtLink(BaseModel):
    source = ForeignKeyField(Thought, backref='links_from')
    target = ForeignKeyField(Thought, backref='links_to')

    class Meta:
        indexes = (
            (('source', 'target'), True),
        )

def init_db():
    db.connect()
    db.create_tables([Thought, Tag, ThoughtTag, Emotion, ThoughtEmotion, ThoughtLink], safe=True)
    db.close()
