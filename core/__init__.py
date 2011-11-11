import sys

from core import config

def print_verbose(msg):
    if config.config.get('verbose',False):
    	print_error(msg)

def print_error(msg):
    sys.stderr.write(str(msg))
    sys.stderr.write('\n')
    sys.stderr.flush()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
