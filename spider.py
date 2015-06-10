import sys
import re
import urllib2
from urllib2 import URLError

# Snow Leopard Fix for threading issues Trace/BPT trap problem
urllib2.install_opener(urllib2.build_opener())
from urlparse import urlparse
import threading
import time
from HTMLParser import HTMLParser


"""
Spider takes a starting URL and  visits all links found within each page
until it doesn't find anymore OR the num links limit is reached
"""
class Spider():
	
	def __init__(self,sUrl, crawl):
	
		#Urlparse has the following attributes: scheme, netloc, path, params,query,fragment
		self.startUrl = urlparse(sUrl)
		self.visitedUrls = {} # Map of link -> page HTML
		self.pendingUrls = {sUrl:sUrl}
		self.startUrlString = sUrl
		self.crawlType = crawl
		self.numBrokenLinks = 0
		self.numTotalLinks = 0
		
	""" Main crawling function that parses the URLs, stores the HTML from each in visitedUrls
		 and analyzes the HTML to acquire and process the links within the HTML"""
	def startcrawling(self):
			
		while 1 and len(self.pendingUrls) > 0:
			try:
				
				self.printProcessed()
			
				currUrl = self.pendingUrls.popitem()[0]		
				
				
				# Make HEAD request first to see if the type is text/html
				url = urllib2.urlopen(HeadRequest(currUrl))
				conType = url.info()['content-type']
				conTypeVal = conType.split(';')
				
				# Only look at pages that have a content-type of 'text/html'
				if conTypeVal[0] == 'text/html':
	
					url = urllib2.urlopen(currUrl)
					html = url.read()
					
					# Map HTML of the current URL in process in the dictionary to the link
					# for further processing if required
					self.visitedUrls[currUrl] = html
					
					# LinksHTMLParser is extended to take out the <a> tags only and store 
					htmlparser = LinksHTMLParser()
					htmlparser.feed(html)
					
					# Check each of the <a> tags found by Parser and store if scheme is http
					# and if it already doesn't exist in the visitedUrls dictionary
					for link in htmlparser.links.keys():	
						url = urlparse(link)
						
						if url.scheme == 'http' and not self.visitedUrls.has_key(link):	
							if self.crawlType == 'local': 
								if url.netloc == self.startUrl.netloc:
									if not self.pendingUrls.has_key(link):
										self.pendingUrls[link] = link
												
							else:	
								if not self.pendingUrls.has_key(link):				
									self.pendingUrls[link] = link
											

			
			# Don't die on exceptions.  Print and move on
			except URLError:
				print "Crawl Exception: URL parsing error" 
				
			except Exception,details:
				print "Crawl Exception: Malformed tag found when parsing HTML"
				print details
				# Even if there was a problem parsing HTML add the link to the list
				self.visitedUrls[currUrl] = 'None'
				
		if self.crawlType == 'local':
			self.numTotalLinks = len(self.visitedUrls)
	
		print "Total number of links: %d" % self.numTotalLinks
		

	""" Helper function to print the number of processed 
		 and pending URLs to STDOUT"""
	def printProcessed(self):
		pendingCount = len(self.pendingUrls.values())
				
		#Limit the amount of pending URLs printed to screen
		if pendingCount %5 == 0:
			print str(pendingCount) + " Pending URLs are in the queue."
			print str(len(self.visitedUrls.values())) + " URLs have been fully processed.\n"
				

	
""" Extend urllib2.Request to add the HEAD method """
class HeadRequest(urllib2.Request):
	def get_method(self):
		return "HEAD"		



""" Extend HTMLparser to provide additional functionality
	  of parsing only <a> tags and holding all the found,
	  non-duplicate links in the links dictionary
	  
	  NOTE: Could use lxml, BeautifulSoup, or other parsers 
	  			  that may not fail as much on broken HTML like
	  			  HTMLParser does.
 """
class LinksHTMLParser(HTMLParser):

	def __init__(self):
		self.links = {}
		self.regex = re.compile('^href$')
		HTMLParser.__init__(self)
		
	
				
	# Pull the <a href> link values out and add to links list
	def handle_starttag(self,tag,attrs):
		if tag == 'a':
			try:
				# Run through the attributes and values appending 
				# tags to the dictionary (only non duplicate links
				# will be appended)
				for (attribute,value) in attrs:
					match = self.regex.match(attribute)
					if match is not None and not self.links.has_key(value):
						self.links[value] = value
						
					
			except Exception,details:
				print "LinksHTMLParser: " 
				print Exception,details

			
if __name__ == "__main__":
	
	
	try:
		
		# Check the url before creating the spider
		url = urlparse(sys.argv[1])
		crawlType = sys.argv[2]
		spider = Spider(sys.argv[1], crawlType)
		spider.startcrawling()
			
	except URLError:
		print "The start URL was invalid. \nUsage: python spider.py [URL] [local|all]\n\t[URL]: In the form http://www.url.to.open.com\n\t[local|all]: local will only crawl the urls that exist in the start site domain - all crawls all links."
	except Exception,details:
		print "The start URL was invalid. \nUsage: python spider.py [URL] [local|all]\n\t[URL]: In the form http://www.url.to.open.com\n\t[local|all]: local will only crawl the urls that exist in the start site domain - all crawls all links."
			


		
	