#!/usr/bin/python

# Startup script
import sys

from core import config
from core import main
from core import print_verbose

if __name__ == "__main__":
    # Build the config to use
    use_config = config.load(sys.argv[1:])
    print_verbose(use_config)
    main.go(use_config)
