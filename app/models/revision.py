from peewee import Model, SqliteDatabase, AutoField, IntegerField, DateTimeField
from datetime import datetime

revision_database = SqliteDatabase("revisions.db")

class Revision(Model):
    class Meta:
        database = revision_database

    id = AutoField()
    animation_id = IntegerField()
    timestamp = DateTimeField(default=datetime.utcnow)

    @classmethod
    def create_for(cls, animation):
        revision =  cls.create(animation_id = animation.id)
        revision.content = animation.content
        return revision

    @classmethod
    def get_revisions_for(cls, animation):
        from .animation import Animation
        id = 0
        if isinstance(animation, Animation):
            id = animation.id
        if isinstance(animation, str):
            _animation = Animation.by_name(animation)
            if _animation:
                id = _animation.id
        if isinstance(animation, int):
            id = animation
        return cls.select().where(cls.animation_id==id).order_by(cls.id.desc())

    @property
    def filepath(self):
        return f"revisions/{self.id}"

    @property
    def animation(self):
        return self.get_animation()

    @property
    def content(self):
        file = open(self.filepath)
        content = file.read()
        return content

    @content.setter
    def content(self, content):
        file = open(self.filepath, "w")
        file.write(content)
        file.close()

    @property
    def size(self):
        return len(self.content)

    def fsize(self):
        dgs = ["B", "KB", "MB"]
        dgi = 0
        s = self.size
        while s > 1024:
            s = round(s/1024, 2)
            dgi += 1
        return f"{s} {dgs[dgi]}"

    def get_animation(self):
        from .animation import Animation
        animation = Animation.get_by_id(self.animation_id)
        return animation

    def rollback(self):
        self.animation.content = self.content


revision_database.create_tables([Revision])
