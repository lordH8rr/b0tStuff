from twill.extensions.check_links import check_links
from selenium import webdriver
from twill.commands import *
import urllib2
import glob
import re
import os

class usR:
	url     = 'http://10.40.24.201/'
	ursname = 'jphelps'
	paswd   = 'jphelps1'
	cookies = None

class commonSites:
	items     = 'imis/MBR/Shop/iCore/Store/StoreLayouts/Store_Home.aspx'
	events    = 'imis/MBR/Events/iCore/Events/Events_List.aspx'
	donations = 'iMIS/MBR/Donate/iCore/Fundraising/Donate_Now.aspx'


def c0nn():
        nu_usr = usR()
	siteCode = urllib2.urlopen(nu_usr.url).getcode()
	
	if(siteCode == 200):
		ItemTest(nu_usr) 
		#EventTest(nu_usr)
		#DonationTest(nu_usr)
		#ContactsTest(nu_usr) 
	else:
		print('Not able to reach %s' %nu_usr.url)	

def ItemTest(usr):
	items = commonSites() 
        itemsUrl = usr.url + items.items
	driver = webdriver.Firefox()
        driver.get(itemsUrl)
	#driver.find_elements_by_xpath("//*[contains(text(), 'text here')]")
	#driver.find_elements_by_partial_link_text('texthere')
	ItemLinksRaw = driver.find_elements_by_tag_name('a')
	ItemLinks    = ItemLinksRaw.text
	print ItemLinksRaw
	
	driver.close()	
 
def EventTest(usr):
	events = connomSites()
	eventsUrl = usr.url + events.events
	driver = webdriver.Firefox()
        driver.get(eventsUrl)
	
	driver.close()

def DonationTest(usr):
	events = connomSites()
        eventsUrl = usr.url + events.events
        driver = webdriver.Firefox()
        driver.get(eventsUrl)

        driver.close()


def AddCart():
	driver.find_element_by_id("").click()


#def CheckOut():


#def ContactTest():



c0nn()
