from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from urllib2 import URLError
import bs4
from bs4 import BeautifulSoup
import urllib2
import re
from colorama import Fore
from colorama import init
#import PublicTests
#import StaffTests
#for colorama
init(autoreset=True)





class SiteDriver(object):
	usrN    = 'jphelps'
	passwd  = 'jphelps1' 
	site    = 'http://10.40.24.223/imis/staff'
	usrType = None
	

	def __init__(self):
		print Fore.CYAN + 'Starting ...'

	
	def MainDriver(self):
		driving = webdriver.Firefox()
		driving.get(SiteDriver.site)	
		wait = WebDriverWait(driving, 10)
		loginTest.login(self, driving)
			

	def StopDriver(self):
		self.driving = driving
		driving.close()


class loginTest(object):
	

		def login(self, driving):
			self.driving = driving
			print Fore.CYAN + '[*] Logging in ...'	

			userRX     = '.*sign*.'
			userUnique = 'User'
			tagType = tagRef.tagTypes[13]	
			usr = beautifulFind(userRX, userUnique, tagType, self, driving)
	
			pwdRX      = '.*sign*.'
			pwdUnique  = 'Pass'
			tagType = tagRef.tagTypes[13]
			pwd = beautifulFind(pwdRX, pwdUnique, tagType, self, driving)

			submitRX      = '.*SubmitButton*.'
			submitUnique  = ''
			tagType = tagRef.tagTypes[0]
			sub = beautifulFind(submitRX, submitUnique, tagType, self, driving)
			
			usrSel = self.driving.find_element_by_id(usr)
			pwdSel = self.driving.find_element_by_id(pwd)
	
			usrSel.send_keys(self.usrN)
			pwdSel.send_keys(self.passwd)
	
			try:
				self.driving.find_element_by_id(sub).click()
				print Fore.CYAN + '[*] Logged in ... '
				
				#self.usrType = check_user(self, driving)				
	
				if self.usrType == 'Public':
					print Fore.BLUE + self.usrType
					#PublicTests.prelimTest(self, driving)	
				else:
					print Fore.BLUE + self.usrType
					#StaffTests.prelimTest(self, driving)

			except NoSuchElementException, e: 
				print Fore.RED + '[*] Failed to submit form: ' + Fore.RED + e
			self.driving.close()

class usr_login(SiteDriver, loginTest):
	pass


class tagRef():
	tagTypes = [None, 'script', 'head', 'body', 'div', 'span', 'a', 'title', 'img', 'area', 'tr', 'td', 'form', 'input', 'button', 'var', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']


def beautifulFind(regex, unique, tagType, self, driving):
	self.driving = driving
	#place the wait here#
	currentSite  = self.driving.current_url	
	soupRDY      = urllib2.urlopen(currentSite).read()
	soup = BeautifulSoup(soupRDY)
	valHold  = []

        for valFind in soup.find_all(tagType, id=re.compile(regex)):
  		valHold.append(valFind.get('id'))
	print valHold


        goodID = [x for x in valHold if unique in x]
        goodID = ''.join(goodID)
	
	print Fore.BLUE + goodID
	
	return goodID


def check_user(self, driving):
        #check for EZ edit
        self.driving = driving
	print Fore.CYAN + 'Checking User .. .. ..'
	 
	userTypeRX       = '.*Error*.'
        userTypeUnique   = ''
        tagType      	 = tagRef.tagTypes[5]
        userTypeFind 	 = beautifulFind(userTypeRX, userTypeUnique, tagType, self, driving)
	
	print userTypeFind
	if userTypeFind != None:
		userType = 'Public'
	else:
		userType = 'Staff'
		
	return userType
	

def check():
	################################################
	check.loginSite = 'http://10.40.25.66/imis/staff'
	#have user type it in live or use config file# 

	try:
		siteCode = urllib2.urlopen(check.loginSite).getcode()
		if(siteCode == 200):
			print Fore.GREEN + '[*] Connected'
			runit = usr_login()
			runit.MainDriver()

	except urllib2.URLError, e:
		print Fore.RED + '[*] Cannot reach site %s \n [*] Site Status: %s ' % (loginSite,e.args) 	
	except urllib2.HTTPError, e:
		print Fore.RED + '[*] Cannot reach site %s \n [*] Site Status: %s ' % (loginSite,e.args)

check()
