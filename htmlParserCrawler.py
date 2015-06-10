import urllib2
import re
from HTMLParser import HTMLParser
from urlparse import urlparse
import threading 
import time



class crawler():

	def __init__(self, sURL, crawlit):
		
		self.startURL = urlparse(sURL)
		self.visited  = {}
		self.pending  = {sURL:sURL}
		self.startURLstring = sURL
		self.crawlType    = crawlit
		self.numBrokenLnk = 0
		self.numTotLnk    = 0

	def startCrawl(self):
		
		while 1 and len(self.pending) > 0:
			try:
				self.printProc()
				#this is printing the status of links#
				currentURL = self.pending.popitem()[0]
	

				#HEAD request using urllib2#
				url = urllib2.urlopen(HeadRequest(currentURL))
				contentType = url.info()['content-type']
				contentTypeValue = contentType.split(';')
				
				#only text/html pages
				if conTypeValue[0] == 'text/html':
					url = urllib2.urlopen(currentURL)
					html = url.read()

					self.visited[currentURL] = html

					#get anchor tags/links
					htmlparser = LinksHTMLParser()
					htmlparser.feed(html)


					for link in htmlparser.links.keys():
						url = urlparse(link)
					
						if url.scheme == 'http' and not self.visited.has_key(link):
							if self.crawlType == 'local':
								if url.netloc == selfstartURL.netloc:
									if not self.pending.has_key(link):
										self.pending[link] = link

							else:
								if not self.pending.has_key(link):
									self.pending[link] = link				
			except URLError:
				print "Url parse error"

			except Exception,details:
				print ""
				print details
				self.visited[currentURL] = 'None'

		if self.crawlType == 'local':
			self.numTotLnk == len(self.visited)

		print "There are %d links" % self.numTotLnk

	

	def printProc(self):
		pendingCount = len(self.pending.values())
		

		if pendingCount %5 == 0:
			print str() + ""
			print str(len()) + ""




class HeaderRequest(urllib2.Request):
	def get_method(self):
		return "HEAD"







class LinksHTMLParser(HTMLParser):

	def __init__(self):
		self.links = {}
		self.regex = re.compile('^href$')
		HTMLParser.__init__(self)


	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			try:
			# go through link dictionary
				for (attribute,value) in attrs:
					match = self.regex.match(attribute)
					if match is not None and not self.link.has_key(value):
						self.links[value] = value

			except Exception,details:
				print "LinksHTMLParser: "
				print Exception,details
	



def main():

	
