import json, datetime

def outputJson():
    file = open("accounts.json", "r")
    out = file.read()
    file.close()
    return out

def getUser(uid):
    file = open("accounts.json", "r")
    json_obj = json.loads(file.read())
    file.close()

    for user in json_obj:
        if uid == user[1]:
            return user
    return None

def addUser(uid):
    file = open("accounts.json", "r")
    json_obj = json.loads(file.read())
    file.close()
    if json_obj: 
        last_num = (json_obj[-1])[0]
    else:
        last_num = -1
    json_obj = json_obj + [[last_num + 1, uid, [], [], [], []]]
    
    file = open("accounts.json", "w")
    file.write(json.dumps(json_obj))
    file.close()

def addProb(uid, prob, numTests):
    file = open("accounts.json", "r")
    json_obj = json.loads(file.read())
    file.close()

    user = getUser(uid)

    expire = datetime.datetime.now() + datetime.timedelta(7,0)
    
    user[2] += [prob]
    user[3] += [datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")]
    user[4] += [expire.strftime("%I:%M%p on %B %d, %Y")]
    user[5] += [numTests]

    json_obj[user[0]] = user

    file = open("accounts.json", "w")
    file.write(json.dumps(json_obj))
    file.close()
