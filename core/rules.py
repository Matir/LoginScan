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

# Define how rules are handled

class LoginScanRule:
    """
    Basic Framework for a LoginScan Rule
    Subclasses MUST implement handle(self,data)
    """
    def __init__(self,config):
        self.config = config

    def handle(self,data,ex=None):
        """
        Handles the response from urllib2.urlopen and/or any HTTPError (ex)
        Should return a tuple of score,message where score is [0,1] and message is an optional message.
        """
        return (0,None)

def loadRule(name):
    """ 
    Loads a class from its name.
    TODO: Validate that the class extends LoginScanRule
    """
    # Have to strip off the class name and just get the module
    mod = '.'.join(name.split('.')[:-1])
    mod = __import__(mod)
    for piece in name.split('.')[1:]:
        mod = getattr(mod,piece)
    return mod

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
