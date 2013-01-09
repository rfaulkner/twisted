
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    A simple web server implemented with the Twisted network programming framework.

    http://twistedmatrix.com/trac/
    http://en.wikipedia.org/wiki/Twisted_(software)

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

import sys
import logging
import argparse

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%b-%d %H:%M:%S')

from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def dataReceived(self, data):
        logging.info("Data received: %s" % str(data))
        self.transport.write(data)

    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)



def main(args):
    reactor.listenTCP(8123, ChatFactory())
    reactor.run()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="This script implements a simple twisted based webserver.",
        epilog="",
        conflict_handler="resolve",
        usage = "./twist.py [-h] [-m METRIC] [-o OUTPUT] [-s DATE_START] [-e DATE_END] [-p PROJECT]"
    )
    # parser.add_argument('-m', '--metric',type=str, help='The metric to compute.',default="bytes_added")

    args = parser.parse_args()

    sys.exit(main(args))