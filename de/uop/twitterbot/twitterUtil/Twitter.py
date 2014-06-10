from twitter import *
from persistance import UserDao, UserTweetDao
import Config


def getMentions():
    t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))
    mentions = t.statuses.mentions_timeline()

    for mention in mentions:
        userId = UserDao.addUser(mention["user"]["screen_name"], mention["user"]["id"])

        if UserTweetDao.isNewUserTweet(mention["id"]):
            UserTweetDao.createUserTweet(userId, mention["id"], mention["text"], mention)