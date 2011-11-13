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

import re
import struct
import sys

import eventlet

from core import net
from core import rules
from core import output
from core import print_verbose,print_error

def go(config):
    """Main function to handle execution"""
    # Dynamically load the configured rules
    ruleset = []
    for r in config['rules'].iterkeys():
        try:
            rule = rules.loadRule(r)
    	    ruleset.append((rule(config),config['rules'][r]))
    	except (ImportError,AttributeError):
            print_error("ERROR: Unable to import rule %s!" % r)
            pass
    config['ruleset'] = ruleset

    # Get outputs
    outputs = output.getOutputs(config['output'])

    # Build the eventlet pool and fire off processing
    pool = eventlet.GreenPool(config['conns'])
    res = pool.starmap(net.handle_url,urllist(config))

    # Sort results and print data
    res = sorted(filter(None,res),key=lambda val: val[1],reverse=True)
    for o in outputs:
    	o.writeall(res)


def hostlist(args):
    """Generator of list of hosts based on arguments from the command line"""
    ip = r'(([0-9]{1,3}\.){3}[0-9]{1,3})'
    iprange = re.compile(ip+'-'+ip+'$')
    cidr = re.compile(ip+'/([0-9]{1,2})$')
    for arg in args:
        # Test for IP range
        m = iprange.match(arg)
        if m:
            # Go over range
            first,last = (net.ip2int(m.groups()[0]),net.ip2int(m.groups()[2]))
            if first>last:
                raise HostError("IP Range is backwards!")
            for ip in xrange(first,last+1):
                yield net.int2ip(ip)
            continue

        # Test for CIDR
        m = cidr.match(arg)
        if m:
            # Expand CIDR
            base,mask = (net.ip2int(m.groups()[0]),int(m.groups()[2]))
            # Convert to bitmask (messy, find better way)
            mask = (1<<(32-mask))-1
            # Skip the network address
            first = (base & ~mask)+1
            last = base | mask
            for ip in xrange(first,last):
            	yield net.int2ip(ip)
            continue

        # Neither is known, return val (hopefully its a single IP or a hostname)
        yield arg


def urllist(config):
    """ 
    Builds arguments to handle_url as tuples for starmap()
    This is a generator, wrapping another generator...
    (config,url)
    """
    if config['source'] == 'hosts':
        for host in hostlist(config['hosts']):
            for proto in 'http','https':
                for port in config[proto]:
                    url = "%s://%s:%s/" % (proto,host,port)
                    yield (config,url)
    elif config['source'] == 'urls':
        for url in config['hosts']:
            yield (config,url)
    elif config['source'] == 'url-file':
        for urlfile in config['hosts']:
            if urlfile == '-':
            	fp = sys.stdin
            else: 
            	try:
                    fp = open(urlfile)
                except (IOError):
                    print_error("Unable to open %s as url list file." % urlfile)
                    continue
            for line in fp:
                yield(config,line.strip())


class HostError(Exception):
    pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
