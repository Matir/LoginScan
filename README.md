LoginScan
---------
Copyright (C) 2011 David Tomaschik <david@systemoverlord.com>

Summary
-------
LoginScan is a python script to scan document roots of webserver for
"interesting" things.  Mostly, it can identify administrative web
interfaces and other similar systems.  LoginScan may be renamed at
some point in the future as it encompasses more functionality.

LoginScan is designed to be flexible: it can do its own scanning of
hosts and ports, or it can take a list of URLs as input to examine.
There are many more options, most of which can be configured either
in a configuration file or at runtime.

LoginScan is intended to be extensible, to allow many rule to be run
against any given set of systems.

LoginScan is NOT intended to eliminate anything from consideration,
only to help prioritize the time and resources of the security
professional.

History
-------
LoginScan was inspired by a talk called "From Low to Pwned" given by
Chris Gates (@carnal0wnage) at B-Sides Atlanta 2011.  Chris related
how seemingly innocous notices from vulnerability scanners (aka "Lows")
can also have serious impacts to the enterprise.

Chris discussed a technique where he builds a list of URLs based on 
open ports returned by the port scanner and then uses Firefox addons
to open all of the URLs and review them manually.  LoginScan was
intended to help prioritize these URLs.

Usage
-----
    usage: loginscan.py [-h] [--http p[,p[..]]] [--https p[,p[..]]] [--verbose]
                        [--conns CONNS] [--timeout TIMEOUT] [--output OUTPUT]
                        [--show-noconn] [--user-agent USER_AGENT]
                        [--urls | --url-file]
                        host [host ...]
    
    Scan document roots for interesting things.
    
    positional arguments:
      host                  Hosts to scan (hostspec)
    
    optional arguments:
      -h, --help            show this help message and exit
      --http p[,p[..]]      Ports to scan with http
      --https p[,p[..]]     Ports to scan with https
      --verbose, -v         Enable extra verbosity
      --conns CONNS, -c CONNS
                            Number of simultaneous connections
      --timeout TIMEOUT, -t TIMEOUT
                            Timeout for connections, in seconds.
      --output OUTPUT, -o OUTPUT
                            Output file name and/or type list.
      --show-noconn         Show failed connections in results.
      --user-agent USER_AGENT, -U USER_AGENT
                            User Agent String to Send with Requests.
      --urls                Treat hostspec as a list of urls to scan, either comma
                            or space separated.
      --url-file            Treat hostspec as a file containing a list of URLs,
                            one per line.
    
    Host specification: - Hosts may be specified as hostnames, - separated ranges,
    or CIDR blocks. - Ranges must have full IPs for start and end. - Hosts may be
    comma or space separated. Ports: - You can provide '0' as a port number to
    disable http or https. - Ports are ignored if a url list is provided. Outputs:
    - Outputs are specified as type=filename. If type= is omitted, text is
    default. - may be specified for standard output. - HTML, CSV, and Plaintext
    outputs are supported. (html,csv,text)
