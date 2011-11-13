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

import os.path
import itertools
import argparse
import ConfigParser

# Set up defaults first
config = {
    'http': [80,8000,8080],
    'https': [443,8443],
    'verbose': False,
	'conns': 20,
    'source': 'hosts',
    'output': 'text=-',

    # Rules
    'rules': {
        'rules.loginscan.httpauth': 10,
        'rules.loginscan.passwordfield': 10,
    }
}

def load(argv):
    """
    First, add from config file, then parse argv
    Any values set in a config file replace the defaults
    To disable a previously-set rule, give it a weight of 0.
    """
    # Parse config files
    cfiles = [ "/etc/loginscan.conf", "/usr/local/etc/loginscan.conf", os.path.expanduser("~/.loginscan.conf"), "loginscan.conf" ]
    parser = ConfigParser.SafeConfigParser()
    readin = parser.read(cfiles)
    if readin:
        # Merge with default_config
        if parser.has_option('loginscan','http'):
        	config['http'] = parser.get('loginscan','http').split(',')
        if parser.has_option('loginscan','https'):
        	config['https'] = parser.get('loginscan','https').split(',')
        if parser.has_option('loginscan','conns'):
        	config['conns'] = parser.getint('loginscan','conns')
        if parser.has_option('loginscan','verbose'):
        	config['verbose'] = parser.getbool('loginscan','verbose')
        # Update rules
        if parser.has_section('rules'):
            config['rules'].update(parser.items('rules'))
            # Delete any rules with weight=0
            rules = {}
            for rule,weight in config['rules'].iteritems():
                if int(weight):
                    rules[rule] = int(weight)
            config['rules'] = rules
            

    # Set up the arg parser
    epilog = """
    Host specification:
    - Hosts may be specified as hostnames, - separated ranges, or CIDR blocks.
    - Ranges must have full IPs for start and end.
    - Hosts may be comma or space separated.
    Ports:
    - You can provide '0' as a port number to disable http or https.
    - Ports are ignored if a url list is provided.
    Outputs:
    - Outputs are specified as type=filename.  If type= is omitted, text is default.  - may be specified for standard output.
    - HTML, CSV, and Plaintext outputs are supported.  (html,csv,text)
    """
    parser = argparse.ArgumentParser(description="Scan document roots for interesting things.",argument_default=argparse.SUPPRESS,epilog=epilog)
    parser.add_argument("--http",type=port_type,help="Ports to scan with http",metavar='p[,p[..]]')
    parser.add_argument("--https",type=port_type,help="Ports to scan with https",metavar='p[,p[..]]')
    parser.add_argument("--verbose","-v",action='store_true',help="Enable extra verbosity")
    parser.add_argument("--conns","-c",type=int,help="Number of simultaneous connections")
    parser.add_argument("--output","-o",help="Output file name and/or type list.")
    sources = parser.add_mutually_exclusive_group()
    urls_help = "Treat hostspec as a list of urls to scan, either comma or space separated."
    sources.add_argument("--urls",help=urls_help,action='store_const',const='urls',dest='source')
    url_file_help = "Treat hostspec as a file containing a list of URLs, one per line."
    sources.add_argument("--url-file",help=url_file_help,action='store_const',const='url-file',dest='source')
    parser.add_argument("hosts",help="Hosts to scan (hostspec)",nargs='+',type=lambda x: x.split(','),metavar='host')

    # Parse The Arguments
    args = parser.parse_args(argv)
    # Merge multiple host lists, we'll deal with ranges later
    args.hosts = itertools.chain(*args.hosts)
    config.update(vars(args).iteritems())

    # Return the compiled config
    return config

def port_type(val):
    """
    Parse ports as an argument, separated by commas
    This could probably be a lambda itself, but might be too complex
    """
    ports = val.split(',')
    ports = filter(lambda x: True if x.isdigit() else False, ports)
    ports = map(int,ports)
    ports = filter(lambda x: True if x>0 and x<65536 else False,ports)
    return ports

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
