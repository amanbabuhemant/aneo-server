from peewee import Model, SqliteDatabase, AutoField, CharField
from hashlib import sha256

user_database = SqliteDatabase("users.db")


class User(Model):
    class Meta:
        database = user_database

    id = AutoField()
    username = CharField(unique=True)
    name = CharField()
    password_hash = CharField(default="")

    @classmethod
    def by_username(cls, username):
        return cls.get_or_none(cls.username == username)

    def set_password(self, password):
        self.password_hash = sha256(password.encode()).hexdigest()
        self.save()

    def match_password(self, password):
        return self.password_hash == sha256(password.encode()).hexdigest()


user_database.create_tables([User])
