from persistance import MysqlManager
import datetime


def create_recommendation(user_tweet_id, full_recommendation, text):
    rec = MysqlManager.Recommendation()
    rec.userTweet = user_tweet_id
    rec.created = datetime.datetime.now()
    rec.updated = datetime.datetime.now()
    rec.fullRecommendation = full_recommendation
    rec.text = text
    rec.status = "new"
    rec.save()

    return rec.id


def get_new_recommendations():
    select = MysqlManager.Recommendation.select().where(MysqlManager.Recommendation.status == "new")
    recs = select.execute()

    return recs


def update_status(rec, status):
    rec.status = status
    rec.updated = datetime.datetime.now()
    rec.save()
