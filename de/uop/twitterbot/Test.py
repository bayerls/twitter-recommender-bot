from persistance import MysqlManager
from twitterUtil import Twitter
from recommender import Recommender
import logging

logging.basicConfig(filename='twitterBot.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# MysqlManager.User.create_table()
# MysqlManager.UserTweet.create_table()
# MysqlManager.Recommendation.create_table()


# Twitter.getMentions()
#
# Recommender.getRecommendation()
#
# Twitter.distributeRecommendations()


try:
    Twitter.read_stream()
except Exception as e:
    print(e)
    logging.exception(e)














