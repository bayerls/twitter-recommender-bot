from peewee import *
import Config


custom_db = MySQLDatabase(port=Config.databasePort, database=Config.databaseDB, user=Config.databaseUser, passwd=Config.databasePW)


class CustomModel(Model):
    class Meta:
        database = custom_db


class User(CustomModel):
    username = CharField(unique=True)
    twitterId = CharField(unique=True)
    userStatus = CharField()
    created = DateTimeField()
    updated = DateTimeField()


class UserTweet(CustomModel):
    user = ForeignKeyField(User, related_name="tweets")
    twitterId = CharField()
    tweet = CharField()
    created = DateTimeField()
    updated = DateTimeField()
    status = CharField()  # new, requested, done
    rawInput = TextField()


class Recommendation(CustomModel):
    userTweet = ForeignKeyField(UserTweet, related_name="recommendations")
    selectedId = CharField()
    created = DateTimeField()
    updated = DateTimeField()
    status = CharField() # new, distributed, discarded
    fullRecommendation = TextField()
    text = CharField()
