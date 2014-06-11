from recommender import Recommender
from persistance import MysqlManager
from twitterUtil import Twitter



# MysqlManager.User.create_table()
# MysqlManager.UserTweet.create_table()
# MysqlManager.Recommendation.create_table()


Twitter.getMentions()

Recommender.getRecommendation()

Twitter.distributeRecommendations()






