#! /usr/bin/env python

import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

from os import curdir, sep
import cgi, sys, re, os, json

PORT = '9001'

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

        if self.headers['Content-type'] == "application/json;charset=utf-8":
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(data_string)
            if not data:
                return        
            if data['mode'] == 'submission':
                self.handle_submission(data)
            elif data['mode'] == 'contribution':
                self.handle_contribution(data)
        
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
            out = open("data/" + fn, 'wb')
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
        print data
        pass

    def handle_contribution(data):
        print "CONTRIBUTION!!"
        print data
        pass

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
    print 'Exiting...\nThank you for using TestIt server!. We sincerely hope you have a pleasant day :)!\n'
    server.socket.close()
    exit(0)
