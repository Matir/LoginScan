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
        return (url,-1,['Unable to connect: %s' % e])

    score = 0
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
