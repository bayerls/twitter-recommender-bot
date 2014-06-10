from twitter import *

from persistance import UserDao, UserTweetDao
import Config



t = Twitter(auth=OAuth(Config.accessToken, Config.accessTokenSecret, Config.apiKey, Config.apiSecret))



#print(t.statuses.user_timeline(screen_name="schlegel_k"))
#print(t.statuses.update(status="Using @sixohsix's sweet Python Twitter Tools."))

#print(t.statuses.home_timeline())

#print(t.statuses.user_timeline())

#print(t.statuses.mentions_timeline())


def getMentions():

    mentions = t.statuses.mentions_timeline()

    for mention in mentions:
        # print(mention["text"])
        # print(mention["created_at"])
        # print(mention["id"])
        # print(mention["lang"])
        # print(mention["user"]["id"])
        # print(mention["user"]["screen_name"])

        userId = UserDao.addUser(mention["user"]["screen_name"], mention["user"]["id"])

        if UserTweetDao.isNewUserTweet(mention["id"]):
            UserTweetDao.createUserTweet(userId, mention["id"], mention["text"])






