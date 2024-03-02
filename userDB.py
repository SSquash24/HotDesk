#User database, exporting functions:

#   users_isValidUID(uid) - returns Boolean
#       is the input uid valid? (correspond to a user)

#   users_getUID(login_creds), returns UID
#       return uid for login_creds of a user
#       if login_creds are invalid, return -1

#   users_getUsername(uid) - returns username
#       PRE: uid is valid

#   UID - integer (all valid UIDs should be non-negative)
#   login_creds - list of 1 element:
#       username: string


# Code below is for testing purposes, will need to be modified!

users = {"James": 0, "Jack": 1, "Sarah": 2}
uidToUsername = {v:k for k,v in users.items()}

# login_creds: list of [username]
#   verifies the login details are correct, and return valid users UID
#   if it is incorrect returns UID -1
def users_getUID(login_creds):
    uid = users.get(login_creds[0])
    if uid == None:
        return -1
    return uid

def users_isValidUID(uid):
    return uid in users.values()

def users_getUsername(uid):
    return uidToUsername[uid]
