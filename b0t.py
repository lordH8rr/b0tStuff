import re
import urllib2
import itertools
import random
import string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class DriverSeat(object):
	#root = 'http://10.40.24.55/iMIS/mbr'	
	#root  = 'http://google.com'
	root = 'http://www.w3schools.com/html/html_forms.asp'


	def __init__(self):
		print 'starting ...'


	def MainDriver(self):
		driving = webdriver.Firefox()
		driving.get(DriverSeat.root)
		self.Crawler(driving)	
	
	def Crawler(self, driving):
		self.driving = driving
		print 'crawling...'
		print 'page lifecycle stuff here'
		print 'see a page, run detection'
		#start detecting bro#
		detectTools.detectTextField(self)
		
		self.StopDriver(self.driving)
						
				##TODO##
		   #start a small crawler here for concept#
				##TODO##

				 #TODO#
        	   #On each page get those detectTools for scraping#
	                         #TODO#
	
	def StopDriver(self, driving):
		print 'closing...'
		self.driving = driving
		driving.close()

class detectTools(object):
	
	def detectTextField(self):
		

		sentence = self.formSentence()
		commonTextFields = self.driving.find_elements_by_tag_name("input")
		
		for fields in commonTextFields:
			try:
				fields.send_keys(sentence)
			except:
				print 'you cant edit this field'
		
		self.detectJSButton()

		
	def formSentence(self):
	
		currentSentence = []
		wc = 0
		sentenceLength  = random.randint(6, 13)
                randSelectWords = random.randint(1, 99154)
                dictFile = 'words'
                openDict = open(dictFile, 'rw+')
                words = openDict.readlines()
                words = map(lambda s: s.strip(), words)

	

		while wc < sentenceLength:	
			randSelectWords = random.randint(1, 99154)
			currentSentence.append(words[randSelectWords])
			print currentSentence
			wc += 1 

		prettyString = ' '.join(currentSentence)
			
		print prettyString
			
		return prettyString


	def detectJSButton(self):
	
		JSButtons = self.driving.find_elements_by_tag_name('button')		
		for buttons in JSButtons:
			try:
				buttons.click()
			except:
				print "Can't click" 
		
		self.detectIFrame()

	def detectIFrame(self):
		IFrames = self.driving.find_elements_by_tag_name('iframe')

		print IFrames 
		##########TODO#########
                #Send to IFrameHandler#
		#######################
		


	def IFrameHandler(self, IFrames):
		self.IFrames = IFrames
		for x in range(len(self.IFrames)):
				##TODO##
			#do some clicking stuff#
				########
			print self.IFrames[x]
		return self.IFrames		
	


	
	def detectSubmit(self):
		##TODO##
                #Find all Buttons#
		Submit = self.find_elements_by_tag_name('submit')
		
		
	####may not need this####
	####def detectNormalButtons(self):
	##########TODO##
        #########Find all JSButtons#
	#########NormalButtons = self.find_elements_by_xpath('//a[@class="Button"]')
		


class StarterMultiHi(DriverSeat, detectTools):
	pass
	


def main():
	
	
	starter = StarterMultiHi()
	starter.MainDriver()
	


		
	
main()
