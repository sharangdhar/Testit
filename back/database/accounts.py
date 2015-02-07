import sqlite3 as lite
import sys

con = 0
cur = 0
profiles = 0
prob = 0

# sets up the connection to the SQLite database
def createDB():
  try:
    con = lite.connect('accounts.db')
  except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
#  finally:
#    if con:
#      con.commit()

  # creates the tables to hold all profile info and problem info
  with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE profiles(uid, name VARCHAR(140), info VARCHAR(140), imgpath VARCHAR(256))')
    profiles = cur.fetchall()
    cur.execute('CREATE TABLE problems(uid, subsol VARCHAR(3), probid, time TIMESTAMP)')
    prob = cur.fetchall()

# add a user's profile to profiles table
def addProfile(uid, name1, info1, imgpath1):
  with con:
    cur = con.cursor()
    cur.execute('INSERT INTO profiles VALUES("+str(uid)+", "+name1+", "+info1+", "+imgpath1+")')

# add problem info to problems table
def addProblem(uid, sbsl, problem, timestmp):
  with con:
    cur = con.cursor()
    cur.execute('INSERT INTO problems VALUES("+str(uid)+", "+sbsl+", "+str(problem)+", "+str(timestmp)")')

# get all profile data for user from profiles table
def getUser(userid):
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM profiles WHERE uid == userid')
    data = cur.fetchall()
    return data

# get all problem data from the problems table
def getProbHist(userid):
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM problems WHERE uid == userid')
    data = cur.fetchall()
    return data

# put together html contents
def getHTML(userid):
  profileinfo = getUser(userid)
  name = profileinfo["name"]
  info = profileinfo["info"]
  imgpath = profileinfo["imgpath"]

  probinfo = getProbHist(userid)
  subsol = probinfo["subsol"]
  probid = probinfo["probid"]
  timestamp = probinfo["time"]
  ret = ""
  return ret
