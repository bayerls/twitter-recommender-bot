from persistance import MysqlManager
import datetime

def createUserTweet(userId, twitterId, tweetInput, rawInput):
    userTweet = MysqlManager.UserTweet()
    userTweet.user = userId
    userTweet.twitterId = twitterId
    userTweet.tweet = tweetInput
    userTweet.created = datetime.datetime.now()
    userTweet.updated = datetime.datetime.now()
    userTweet.status = "new"
    userTweet.rawInput = rawInput
    userTweet.save()

    return userTweet.id


def getUserTweetByTwitterId(twitterId):

    try:
        userTweet = MysqlManager.UserTweet.get(MysqlManager.User.twitterId == twitterId)
    except Exception:
        userTweet = None
        #print("userTweet not found: " + str(twitterId))

    return userTweet

def isNewUserTweet(twitterId):
    tweet = getUserTweetByTwitterId(twitterId)

    if tweet is not None:
        return False
    else:
        return True

def getNewUserTweets():
    select = MysqlManager.UserTweet.select().where(MysqlManager.UserTweet.status == "new")
    ut = select.execute()

    return ut

def updateStatus(userTweet, status):
    userTweet.status = status
    userTweet.updated = datetime.datetime.now()
    userTweet.save()


