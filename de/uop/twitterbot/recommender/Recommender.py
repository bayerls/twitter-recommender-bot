import requests
from persistance import RecommendationDao, UserTweetDao
import Config
from twitterUtil import Twitter
import ast

dev = "http://eexcess-dev.joanneum.at/eexcess-privacy-proxy/api/v1/recommend"
payloadPrefix = '{"eexcess-user-profile": {"interests": {"interest": []},"context-list": {"context": ['
payloadSuffix = ']}}}'


def getRecommendation():
    newTweets = UserTweetDao.getNewUserTweets()

    for tweet in newTweets:
        UserTweetDao.updateStatus(tweet, "requested")
        recInputList = getRecInputFromTweet(tweet)
        rec = recommend(recInputList)

        if rec is not None:
            text = getRecTextForTweet(tweet, rec)
            RecommendationDao.createRecommendation(tweet.id, rec.getFullRec(), text)
            UserTweetDao.updateStatus(tweet, "done")
        else:
            UserTweetDao.updateStatus(tweet, "noRecommendation")


def getRecTextForTweet(tweet, rec):
    urlLength = min(len(rec.getURI()), Twitter.getMaxUrlLength())
    text = "@" + tweet.user.username + " Look: "
    prefixLength = len(text) + urlLength + 1
    lengthLeft = 140 - prefixLength

    if len(rec.getTitle()) > lengthLeft:
        desc = rec.getTitle()[0:lengthLeft - 2] + "..."
    else:
        desc = rec.getTitle()

    text = text + rec.getURI() + " " + desc

    return text


def getRecInputFromTweet(tweet):
    # t = ast.literal_eval(tweet.rawInput)
    # print(tweet.rawInput)
    # print(t["entities"]["hashtags"])
    # print(t["entities"]["user_mentions"])

    keywords = getKeywords(tweet.tweet)

    recInputList = []

    for keyword in keywords:
        recInput = RecInput()
        recInput.setText(keyword)
        recInput.setWeight(1.0)
        recInputList.append(recInput)

    return recInputList


def getKeywords(tweet):
    # remove mention of the bot
    tweet = tweet.replace(Config.name, "")
    # remove # and @
    tweet = tweet.replace("#", "")
    tweet = tweet.replace("@", "")

    return tweet.split()


def recommend(listRecInput):
    #generate payload
    payload = generatePayload(listRecInput)
    # print("payload: " + payload)

    # Query backend
    r = requests.post(dev, data=payload)
    # print("response: " + str(r.json()))

    # extract recs
    recommendation = extractRecommendation(r.json())
    # print("recommendation: " + recommendation.getURI() + " - " + recommendation.getTitle())

    return recommendation


def generatePayload(listRecInput):
    payload = payloadPrefix

    for input in listRecInput:
        payload += '{"weight":"' + str(input.getWeight()) + '","text":"' + input.getText() + '"},'

    # remove last comma
    payload = payload[:-1]
    payload += payloadSuffix

    return payload


def extractRecommendation(json):
    recommendation = None

    if int(json["totalResults"]) > 0:
        recommendation = Recommendation()
        recommendation.setURI(json["results"][0]["uri"])
        recommendation.setTitle(json["results"][0]["title"])
        recommendation.setFullRec(json)

    return recommendation


class Recommendation:
    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def setURI(self, uri):
        self.uri = uri

    def getURI(self):
        return self.uri

    def setFullRec(self, fullRec):
        self.fullRec = fullRec

    def getFullRec(self):
        return self.fullRec


class RecInput:
    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight