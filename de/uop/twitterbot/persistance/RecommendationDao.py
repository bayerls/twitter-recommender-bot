from persistance import MysqlManager
import datetime


def createRecommendation(userTweetId, fullRecommendation, text):
    rec = MysqlManager.Recommendation()
    rec.userTweet = userTweetId
    rec.created = datetime.datetime.now()
    rec.updated = datetime.datetime.now()
    rec.fullRecommendation = fullRecommendation
    rec.text = text
    rec.status = "new"
    rec.save()

    return rec.id


def getNewRecommendations():
    select = MysqlManager.Recommendation.select().where(MysqlManager.Recommendation.status == "new")
    recs = select.execute()

    return recs


def updateStatus(rec, status):
    rec.status = status
    rec.updated = datetime.datetime.now()
    rec.save()
