#! /usr/bin/env python

import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

from os import curdir, sep
import cgi

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
            if self.path.endswith(".css"):
                mime='text/css'

            if mime:
                #Open the static file requested and send it
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
            if self.path=="/send":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                             'CONTENT_TYPE':self.headers['Content-Type'],
                         })

                print "Your name is: %s" % form["your_name"].value
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Thanks %s !" % form["your_name"].value)
            return			


try:
    server = BaseHTTPServer.HTTPServer(('', 9001), handler)
    print 'Starting TestIt server on port ' + PORT + '!'
    server.serve_forever()

except KeyboardInterrupt:
    print 'Exiting...\n'
    server.socket.close()
    exit(0)
