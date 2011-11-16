# Copyright (C) 2011 by David Tomaschik <david@systemoverlord.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from eventlet.green import socket
from eventlet.green import urllib2
import struct

from core import rules

def handle_url(config,url):
    """Handle a single url"""
    res = None
    ex = None
    messages = []

    try:
        res = urllib2.urlopen(url)
    except urllib2.HTTPError as ex:
        pass
    except urllib2.URLError as e:
        if config['show_noconn']:
            return (url,-1,['Unable to connect: %s' % e])
        return None

    score = 0

    # Copy the data out once
    if res:
    	res.body = res.read()

    for rule,weight in config['ruleset']:
    	rscore,message = rule.handle(res,ex)
        score += weight * rscore
        if message:
            messages.append(message)

    return (url,score,messages)
    

def ip2int(ip):
    """Convert IP as string to integer."""
    return struct.unpack('!L',socket.inet_aton(ip))[0]

def int2ip(val):
    """Convert integer to IP string."""
    return socket.inet_ntoa(struct.pack('!L',val))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
