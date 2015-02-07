#! /usr/bin/env python

import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

from os import curdir, sep
import cgi, sys, re, os, json, zipfile, subprocess, random
import accounts

PORT = '9001'
tid = 0

class handler (BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path=="/":
            self.path="/client/index.html"
        else:
            self.path="/client" + self.path

        try:
            mime = None
            if self.path.endswith(".html"):
                mime='text/html'
            if self.path.endswith(".js"):
                mime='application/javascript'
            if self.path.endswith(".jpg"):
                mime='image/jpg'
            if self.path.endswith(".gif"):
                mime='image/gif'
            if self.path.endswith(".png"):
                mime='image/png'
            if self.path.endswith(".css"):
                mime='text/css'

            if mime:
                file = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mime)
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
                return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        match = re.search(u"application/json", self.headers['Content-type'])

        if not match == None:
            data_string = self.rfile.read(int(self.headers['Content-length']))
            data = json.loads(data_string)
            if not data:
                return
            if data['mode'] == 'login':
                self.handle_login(data)
            if data['mode'] == 'submission':
                global tid
                try: 
                    check = open("data/checks/check_" + str(tid) + ".json", "w")
                    check.write(data_string)
                    check.close()
                except:
                    return
                self.handle_submission(data)
            elif data['mode'] == 'contributor_tid':
                self.handle_contributor_tid(data)
            elif data['mode'] == 'contributor_check':
                self.handle_contributor_check(data)
            elif data['mode'] == 'contributor_tests':
                self.handle_contributor_tests(data)
        else:
            self.deal_post_data()


    # From https://gist.github.com/UniIsland/3346170
    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.path
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open("data/env/env_" + str(tid) + ".zip", 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def handle_submission(self, data):
        print "SUBMISSION!!"
        global tid

        try:
            env = zipfile.ZipFile("data/env/env_" + str(tid) + ".zip", "r")
            if not os.path.exists("data/env/env_" + str(tid)):
                os.mkdir("data/env/env_" + str(tid))
            else:
                os.system("rm -rf data/env/env_" + str(tid))
                os.mkdir("data/env/env_" + str(tid))
            env.extractall("data/env/env_" + str(tid) + "/")
            os.remove("data/env/env_" + str(tid) + ".zip")
        except:
            self.wfile.write("File submitted was not a zip file!")
            return

        if not os.path.exists("data/env/env_" + str(tid) + "/testit.py"):
            self.wfile.write("testit.py not found in submitted environment zip file!")
            return

        file = open("data/env/env_" + str(tid) + "/testit.py", "a")
        file.write("\n\n")

        file.write("assert( " + data['tests'][0]['a10'] + data['tests'][0]['a11'] 
                   + data['tests'][0]['a12'] +" )\n")
        file.write("assert( " + data['tests'][1]['a20'] + data['tests'][1]['a21'] 
                   + data['tests'][1]['a22'] + " )\n")
        file.write("assert( " + data['tests'][2]['a30'] + data['tests'][2]['a31'] 
                   + data['tests'][2]['a32'] + " )\n")

        file.close()

        try:
            os.chdir("data/env/env_" + str(tid))
            x = subprocess.check_call(["python", "testit.py"])
            self.wfile.write("All tests passed!")
            tid = tid + 1
        except:      
            self.wfile.write("One or more test cases failed!")
            os.system("rm -rf data/env/env_" + str(tid))

        os.chdir("../../..")

    def handle_contributor_tid(self, data):
        print "GETTING TID!!"
        global tid
        if (tid == 0):
            self.wfile.write("-1")
        else:
            tid_local = 0
            while (tid_local < tid):
                if os.path.exists("data/results/result_" + str(tid_local)):
                    file = open("data/results/result_" + str(tid_local), "r")
                    json_obj = json.loads(file.read())
                    file.close()
                    if json_obj[data['uid']] == None:
                        break
                else:
                    break
                tid_local = tid_local + 1

            if tid_local >= tid:
                self.wfile.write("-1")
                return

            if os.path.exists("data/checks/check_" + str(tid_local) + ".json"):
                file = open("data/checks/check_" + str(tid_local) + ".json", "r")                
                json_obj = json.loads(file.read())
                file.close()
                json_obj['problem_id'] = str(tid_local)
                self.wfile.write(json.dumps(json_obj))
            else:
                self.wfile.write("-1")
                return


    def handle_contributor_check(self, data):
        print "CONTRIBUTION!!"
        
        tid = data['problem_id']

        all_tests = data['tests']
        
        os.chdir("data/env/env_" + str(tid))
        file = open("testit.py", "a")
        pos = file.tell()

        for test in all_tests:
            file.write("\n\n")
            file.write("assert("+test[0]+test[1]+test[2]+" )\n")

        file.close()

        try:
            x=subprocess.check_call(["python", "testit.py"])
            self.wfile.write("All tests passed!")
        except:
            self.wfile.write("One or more test cases failed!")

        file = open("testit.py", "a")
        file.seek(pos, os.SEEK_SET)
        file.truncate(pos)
        file.close()
        os.chdir("../../..")

    def handle_contributor_tests(self, data):
        print "Success"
        
        tid = data['problem_id']
        
        all_tests = data['tests']
        user_setup = data['setup']
        arr = []
        i=0

        file = open("data/env/env_" + str(tid) + "/testit.py", "a")
        file.write("\n\n")
        file.write(user_setup)
        file.write("\n\n")
        os.chdir("data/env/env_" + str(tid))
        pos = file.tell()

        for test in all_tests:
            file.write("assert("+test[0]+test[1]+test[2]+" )\n")
            file.close()

            try:
                x=subprocess.check_call(["python", "testit.py"])
                arr = arr + [((test[0]+test[1]+test[2]).encode('utf-8'), "Passed")]
            except:
                arr = arr + [((test[0]+test[1]+test[2]).encode('utf-8'), "Failed")]
            i=i+1
            file = open("testit.py", "a")
            file.seek(pos, os.SEEK_SET)
            file.truncate(pos)

        os.chdir("../../..")
        file.close()

        if os.path.exists("data/results/result_" + str(tid)):
            file = open("data/results/result_" + str(tid), "r")
            json_obj = json.loads(file.read())
            file.close()
        else:
            json_obj = {}

        json_obj[data['uid']] = arr

        file = open("data/results/result_" + str(tid), "wb")
        file.write(json.dumps(json_obj))
        self.wfile.write(json.dumps(json_obj[data['uid']]))

        addProb(data['uid'], str(tid), len(all_tests))

        file.close()

    def handle_login(self, data):
        print data['uid']
        if getUser(data['uid']) == None:
            addUser(data['uid'])
        else:
            return

    def log_message(self, format, *args):
        log = open(".log", 'a')
        log.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args)) 
        log.close()
        return


try:
    server = BaseHTTPServer.HTTPServer(('', 9001), handler)
    print 'Starting TestIt server on port ' + PORT + '!\n'
    server.serve_forever()

except KeyboardInterrupt:
    print 'Exiting...\nThank you for using TestIt server! We sincerely hope you have a pleasant day :)!\n'
    os.system("rm -rf data/env/* data/checks/* data/results/*")
    server.socket.close()
    exit(0)
