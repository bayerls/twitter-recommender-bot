from recommender import Recommender
from persistance import UserDao, UserTweetDao, RecommendationDao


listRecInput = []


# recInput1 = Recommender.RecInput()
# recInput1.setText("Europa")
# recInput1.setWeight(1.0)
# listRecInput.append(recInput1)
#
# recInput2 = Recommender.RecInput()
# recInput2.setText("Berlin")
# recInput2.setWeight(1.0)
# listRecInput.append(recInput2)
#
# recommendation = Recommender.recommend(listRecInput)
#
# if recommendation is not None:
#     print(recommendation.getTitle())

RecommendationDao.createRecommendation(UserTweetDao.createUserTweet(UserDao.createUser("basti2"), "MessageTweet2"), "recFull")



