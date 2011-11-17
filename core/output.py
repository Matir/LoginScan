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

import sys
from core import print_error

def getOutputs(options):
    outputmap = {
        'text':     GenericOutput,
        'generic':  GenericOutput,
        'csv':      CSVOutput,
        'html':     HTMLOutput,
    }
    outputs = []
    for opt in options.split(','):
        if '=' in opt:
            otype,dest = opt.split('=')
            try:
                outputs.append(outputmap[otype](dest))
            except (KeyError):
                # TODO: Turn this into a custom error
                raise
        else:
            outputs.append(GenericOutput(opt))
    # Full list
    return outputs
    

class GenericOutput(object):
    """
    Generic output class, does text based output.
    Should be extended for other classes.
    Generally, overload write(), header(), footer()
    """
    def __init__(self,fname):
        self.openfp(fname)
        self.header()

    def openfp(self,fname): 
        """Open the output file for writing"""
        if not fname or fname == '-':
            self.fp = sys.stdout
        else:
            try:
                self.fp = open(fname,"w")
            except (IOError):
                print_error("Unable to open file for output:" % fname)
                raise

    def write(self,entry):
        """Write a single entry to output, taking a tuple."""
        self.fp.write("%-32s %5d %4s %s\n" % (entry[0],entry[1],entry[2] if entry[2] else '',' '.join(entry[3])))

    def writeall(self,data):
        """Write all entries"""
        for entry in data:
            self.write(entry)
        self.footer()

    def header(self):
        """Write a header"""
        self.fp.write("%-32s %5s %4s %s\n" % ("URL","Score","HTTP","Notes"))

    def footer(self):
        """Write a footer if needed"""
        pass


class CSVOutput(GenericOutput):
    """
    Write out to a csv.
    """

    def write(self,entry):
        self.fp.write("\"%s\",\"%d\",\"%s\",\"%s\"\n" % (entry[0],entry[1],entry[2] if entry[2] else '',';'.join(entry[3])))

    def header(self):
        self.fp.write('"URL","Score","HTTP","Notes"\n')


class HTMLOutput(GenericOutput):
    """
    Write out to HTML.
    """

    def header(self):
        self.fp.write("<html><head><title>LoginScan Report</title></head><body><table>");
        self.fp.write("<tr><th>URL</th><th>Score</th><th>HTTP Status</th><th>Notes</th></tr>")

    def write(self,entry):
        self.fp.write("<tr><td><a href='%s'>%s</a></td><td>%d</td><td>%s</td><td>%s</td></tr>" % 
                (entry[0],entry[0],entry[1],entry[2] if entry[2] else '','<br />'.join(entry[3])))

    def footer(self):
        self.fp.write("</table></body></html>")

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
