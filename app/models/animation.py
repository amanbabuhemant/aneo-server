from peewee import Model, SqliteDatabase, AutoField, CharField, DateTimeField, TextField, BooleanField
from datetime import datetime
from hashlib import sha256


animation_database = SqliteDatabase("animations.db")


class Animation(Model):
    class Meta:
        database = animation_database

    id = AutoField()
    name = CharField(unique=True)
    title = CharField()
    created = DateTimeField(default=datetime.utcnow)
    updated = DateTimeField(default=datetime.utcnow)
    content_hash = CharField(default="")
    active = BooleanField(default=False)

    def __repr__(self):
        return f"<Animation: {self.name}>"

    def __str__(self):
        return self.content

    @staticmethod
    def valid_name(name: str) -> bool:
        valid_chars = "abcdefghijklmnopqrstuvwxyz-"
        for c in name:
            if c not in valid_chars:
                return False
        return True

    @classmethod
    def by_name(cls, name):
        return cls.get_or_none(cls.name == name)

    @property
    def filepath(self):
        return "animations/" + self.name + ".lua"

    @property
    def content(self):
        return self.get_content()

    @content.setter
    def content(self, content):
        return self.set_content(content)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def get_content(self):
        try:
            file = open(self.filepath)
        except:
            return ""
        content = file.read()
        file.close()
        return content

    def set_content(self, content):
        file = open(self.filepath, "w")
        file.write(content)
        file.close()
        hash = sha256(self.content.encode()).hexdigest()
        self.content_hash = hash
        self.save()
        return self.verify_content()

    def verify_content(self):
        content = self.get_content()
        hash = sha256(content.encode()).hexdigest()
        return hash == self.content_hash
    


animation_database.create_tables([Animation])
