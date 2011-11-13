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

# Default ruleset
import HTMLParser

from core import rules

class dummy(rules.LoginScanRule):
	""" Dummy rule, just prints data """
	def handle(self,data,ex=None):
		"""Handle a urllib2 response"""
		if data:
			print data.geturl()
			print data.info().headers
			print data.read()
		print dir(ex)
		return (0,None)

class httpauth(rules.LoginScanRule):
	""" Check for 401 authentication """
	def handle(self,data,ex=None):
		if not ex:
			return (0,None)
		if ex.getcode() != 401:
			return (0,None)
		info = ex.info().getheader('WWW-Authenticate')
		return (1,'HTTP Authentication: %s' % info)

class passwordfield(rules.LoginScanRule):
	""" Look for an HTML password field """
	def handle(self,data,ex=None):
		# Check if we got data at all
		if not data:
			return (0,None)

		parser = PasswordParser()
		parser.feed(data.read())
		res = parser.close()
		if res:
			return (1,'Password field found: %s' % res)

		return (0,None)


# special class for HTML parser
class PasswordParser(HTMLParser.HTMLParser):
	# Set the flag
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.foundpw = False

	# Handle operations at the end
	def close(self):
		HTMLParser.HTMLParser.close(self)
		return self.foundpw

	def handle_starttag(self,tag,attrs):
		if tag != 'input':
			return
		attrs = dict(attrs)
		if attrs.get('type','').lower() == "password":
			self.foundpw = attrs.get('name',True)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
