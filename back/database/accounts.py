import sqlite3 as lite
import sys, json

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
def addProfile(uid1, name1, info1, imgpath1):
  con = lite.connect('accounts.db')
  with con:
    cur = con.cursor()
    params = (str(uid1), name1, info1, imgpath1)
    cur.execute("INSERT INTO profiles VALUES(?,?,?,?)", params)

# add problem info to problems table
def addProblem(uid1, subsol1, probid1, time1):
  con = lite.connect('accounts.db')
  with con:
    cur = con.cursor()
    params = (str(uid), subsol1, str(pobid1), str(time1));
    cur.execute("INSERT INTO problems VALUES(?,?,?,?)", params)

# get all profile data for user from profiles table
def getUser(userid):
  con = lite.connect('accounts.db')
  with con:
    cur = con.cursor()
    param = (str(userid),)
    cur.execute('SELECT * FROM profiles WHERE uid = ?', param)
    data = cur.fetchall()
    return data

# get all problem data from the problems table
def getProbHist(userid):
  con = lite.connect('accounts.db')
  with con:
    cur = con.cursor()
    param = (str(userid),)
    cur.execute('SELECT * FROM problems WHERE uid = ?', param)
    data = cur.fetchall()
    return data

# put together html contents
def getjson(userid):
  profileinfo = getUser(userid)
  name = (profileinfo[0])[1]
  info = (profileinfo[0])[2]
  imgpath = (profileinfo[0])[3]

  probinfo = getProbHist(userid)
  subsol = ''
  probid = ''
  timestamp = ''
  ret = '[';
  first =True;
  for row in probinfo:
    subsol = (row)[1]
    probid = (row)[2]
    timestamp = (row)[3]
    ret = ', {subsol: '+subsol+', time: '+time+'}'
    if first:
      ret = ret[2:]
      first = false
  ret = ret+']'
  '''  ret = <div class = "container">
             <div class = "raw">
               <img src = '+imgpath+'>
               <H3 class = "col-md-3 col-md-offset-3">'+name+'</H3>
               <Br>
               <H4 class = "col-md-2 col-md-offset-2">'+info+'</H4>
             </div>
             <div class = "raw">
               <table>
                 <th>
                   <td>'+probid+'</td>
                   <td>'+timstamp+'</td>
                 </th>
                 <tr>
                   <td>'+'____'+'</td>
                   <td>'+'____'+'</td>
                   <td>'+'____'+'</td>
                 </tr>
               </table>
             </div>
           </div>
  '''
  return ret
