from twitter import *
from persistance import UserDao, UserTweetDao, RecommendationDao
import Config
from recommender import Recommender


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
        t.statuses.update(status=rec.text, in_reply_to_status_id=rec.userTweet.user.twitterId)  # TODO not working?
        RecommendationDao.updateStatus(rec, "done")


def getMaxUrlLength():
    t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))

    return t.help.configuration()["short_url_length_https"]


def readStream():
    twitter_userstream = TwitterStream(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret), domain='userstream.twitter.com')

    for msg in twitter_userstream.user():
        recommend = False

        if "entities" in msg:
            for mention in msg["entities"]["user_mentions"]:
                if mention["screen_name"] == Config.name.replace("@", ""):
                    recommend = True

            if recommend:
                userId = UserDao.addUser(msg["user"]["screen_name"], msg["user"]["id"])
                UserTweetDao.createUserTweet(userId, msg["id"], msg["text"], msg)
                Recommender.getRecommendation()
                distributeRecommendations()

        # 'event': 'follow',


def getCurrentLimit():
    t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))

    print(t.application.rate_limit_status())

    #  TODO does statuses update return something? How many remaining updates possible?
