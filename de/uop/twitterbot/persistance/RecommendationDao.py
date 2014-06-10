from persistance import MysqlManager
import datetime


def createRecommendation(userTweetId, fullRecommendation):
    rec = MysqlManager.Recommendation()
    rec.userTweet = userTweetId
    rec.created = datetime.datetime.now()
    rec.updated = datetime.datetime.now()
    rec.fullRecommendation = fullRecommendation
    rec.save()

    return rec.id
