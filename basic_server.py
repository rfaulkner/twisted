
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    A simple web server implemented with the Python native libraries.

    code adapted from http://fragments.turtlemeat.com/pythonwebserver.php

"""
__author__ = "ryan faulkner"
__date__ = "01/08/2013"
__license__ = """\
Copyright (c) 2013 Ryan Faulkner <rfaulkner@wikimedia.org>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.\
"""


import cgi
import time
import sys
import logging
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%b-%d %H:%M:%S')

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        logging.info('Processing GET: %s in %s' % (self.headers, self.path))
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".esp"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(str(time.localtime()[7]))
                self.wfile.write(str(time.localtime()[0]))
                return
            return

        except IOError:
            self.send_error(404, 'File not found: %s ' % self.path)

    def do_POST(self):
        global rootnode
        logging.info('Processing POST: %s in %s' % (self.headers, self.path))
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            query = None
            if ctype == 'mukltipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)

            if query:
                self.end_headers()
                upfilecontent = query.get('upfile')
                logging.info('filecontent', upfilecontent[0])
                self.wfile.write("<HTML>POST OK.<br><br>")
                self.write(upfilecontent[0])
            else:
                self.send_error(404, 'File not found.')

        except Exception: pass

def main():
    server = None
    try:
        server = HTTPServer(('',1234), MyHandler)
        logging.info('Starting server ...')
        server.serve_forever()
    except KeyboardInterrupt:
        if server:
            logging.info('^C received, shitting down...')
            server.socket.close()
        else:
            logging.error('Could not initialize server.')

if __name__ == "__main__":
    sys.exit(main())



