import requests
from persistance import RecommendationDao, UserTweetDao, Enums
import Config

dev = "http://eexcess-dev.joanneum.at/eexcess-privacy-proxy/api/v1/recommend"
payload_prefix = '{"eexcess-user-profile": {"interests": {"interest": []},"context-list": {"context": ['
payload_suffix = ']}}}'


def get_recommendation():
    new_tweets = UserTweetDao.get_new_user_tweets()

    for tweet in new_tweets:
        UserTweetDao.update_status(tweet, Enums.UserTweetStatus.requested)
        rec_input_list = get_rec_input_from_tweet(tweet)

        rec = None

        if len(rec_input_list) > 0:
            rec = recommend(rec_input_list)

        if rec is not None:
            text = get_rec_text_for_tweet(tweet, rec)
            RecommendationDao.create_recommendation(tweet.id, rec.getFullRec(), text)
            UserTweetDao.update_status(tweet, Enums.UserTweetStatus.done)
        else:
            UserTweetDao.update_status(tweet, Enums.UserTweetStatus.no_recommendation)


def get_rec_text_for_tweet(tweet, rec):
    twitter_max_length = 23  # Twitter.getMaxUrlLength()
    url_length = min(len(rec.getURI()), twitter_max_length)
    text = "@" + tweet.user.username + " Look: "
    prefix_length = len(text) + url_length + 1
    length_left = 140 - prefix_length

    if len(rec.getTitle()) > length_left:
        desc = rec.getTitle()[0:length_left - 2] + "..."
    else:
        desc = rec.getTitle()

    text = text + rec.getURI() + " " + desc

    return text


def get_rec_input_from_tweet(tweet):
    # t = ast.literal_eval(tweet.rawInput)
    # print(tweet.rawInput)
    # print(t["entities"]["hashtags"])
    # print(t["entities"]["user_mentions"])

    keywords = get_keywords(tweet.tweet)
    stop_words = [line.strip() for line in open('english')]
    filtered_keywords = []

    for keyword in keywords:
        if keyword.lower() not in stop_words:
            filtered_keywords.append(keyword)

    rec_input_list = []

    for keyword in filtered_keywords:
        rec_input = RecInput()
        rec_input.setText(keyword)
        rec_input.setWeight(1.0)
        rec_input_list.append(rec_input)

    return rec_input_list


def get_keywords(tweet):
    # remove mention of the bot
    tweet = tweet.replace(Config.name, "")
    # remove # and @
    tweet = tweet.replace("#", "")
    tweet = tweet.replace("@", "")

    return tweet.split()


def recommend(list_rec_input):
    #generate payload
    payload = generate_payload(list_rec_input)
    # print("payload: " + payload)

    # Query backend
    r = requests.post(dev, data=payload)
    # print("response: " + str(r.json()))

    # extract recs
    recommendation = extract_recommendation(r.json())
    # print("recommendation: " + recommendation.getURI() + " - " + recommendation.getTitle())

    return recommendation


def generate_payload(list_rec_input):
    payload = payload_prefix

    for rec_input in list_rec_input:
        payload += '{"weight":"' + str(rec_input.getWeight()) + '","text":"' + rec_input.getText() + '"},'

    # remove last comma
    payload = payload[:-1]
    payload += payload_suffix

    return payload


def extract_recommendation(json):
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