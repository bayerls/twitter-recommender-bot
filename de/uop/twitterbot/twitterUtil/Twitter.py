from twitter import *
from persistance import UserDao, UserTweetDao, RecommendationDao
import Config


def getMentions():
    t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))
    mentions = t.statuses.mentions_timeline()

    for mention in mentions:
        userId = UserDao.addUser(mention["user"]["screen_name"], mention["user"]["id"])

        if UserTweetDao.isNewUserTweet(mention["id"]):
            UserTweetDao.createUserTweet(userId, mention["id"], mention["text"], mention)


def distributeRecommendations():
    t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))
    recs = RecommendationDao.getNewRecommendations()

    for rec in recs:
        t.statuses.update(status=rec.text)
        RecommendationDao.updateStatus(rec, "done")


def getMaxUrlLength():
    t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))

    return t.help.configuration()["short_url_length_https"]
