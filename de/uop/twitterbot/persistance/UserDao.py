from persistance import MysqlManager
import datetime


def createUser(username, twitterId):
    user = MysqlManager.User()
    user.username = username
    user.twitterId = twitterId
    user.created = datetime.datetime.now()
    user.updated = datetime.datetime.now()
    user.userStatus = "normal"
    user.save()

    return user.id

def addUser(username, twitterId):
    user = getUserByTwitterId(twitterId)

    if user is None:
        id = createUser(username, twitterId)
    else:
        id = user.id

    return id




def update(twitterId):
    user = getUserByTwitterId(twitterId)

    if user is not None:
        user.updated = datetime.datetime.now()
        user.save()



# def updateUserStatus(username, userStatus):
#     update = MysqlManager.User.update(userStatus=userStatus).where(MysqlManager.User.username == username)
#
#
#     user.updated = datetime.datetime.now()
#     update.execute()


def getUserByTwitterId(twitterId):


    try:
        user = MysqlManager.User.get(MysqlManager.User.twitterId == twitterId)
    except Exception:
        user = None
        #print("user not found: " + str(twitterId))

    return user

