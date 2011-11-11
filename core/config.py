import os.path
import itertools
import argparse
import ConfigParser

# Set up defaults first
config = {
    'http': [80,8000,8080],
    'https': [443,8443],
    'dns': True,
    'verbose': False,
	'conns': 20,

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
        if parser.has_option('loginscan','dns'):
        	config['dns'] = parser.getbool('loginscan','dns')
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
    Hosts may be specified as hostnames, - separated ranges, or CIDR blocks.
    Ranges must have full IPs for start and end.
    Hosts may be comma or space separated.
    You can provide '0' as a port number to disable http or https.
    """
    parser = argparse.ArgumentParser(description="Scan document roots for interesting things.",argument_default=argparse.SUPPRESS,epilog=epilog)
    parser.add_argument("--http",type=port_type,help="Ports to scan with http",metavar='p[,p[..]]')
    parser.add_argument("--https",type=port_type,help="Ports to scan with https",metavar='p[,p[..]]')
    parser.add_argument("--no-dns",action='store_false',help="Disable all DNS queries",dest='dns')
    parser.add_argument("--verbose","-v",action='store_true',help="Enable extra verbosity")
    parser.add_argument("--conns","-c",type=int,help="Number of simultaneous connections")
    parser.add_argument("hosts",help="Hosts to scan",nargs='+',type=lambda x: x.split(','))

    # Parse The Arguments
    args = parser.parse_args(argv)
    # Merge multiple host lists, we'll deal with ranges later
    args.hosts = [x for x in itertools.chain(*args.hosts)]
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
