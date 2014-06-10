import requests

dev = "http://eexcess-dev.joanneum.at/eexcess-privacy-proxy/api/v1/recommend"
payloadPrefix = '{"eexcess-user-profile": {"interests": {"interest": []},"context-list": {"context": ['
payloadSuffix = ']}}}'

def recommend(listRecInput):
    #generate payload
    payload = generatePayload(listRecInput)
    print("payload: " + payload)

    # Query backend
    r = requests.post(dev, data=payload)
    print("response: " + str(r.json()))

    # extract recs
    recommendation = extractRecommendation(r.json())
    print("recommendation: " + recommendation.getURI() + " - " + recommendation.getTitle())

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


class RecInput:
    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight