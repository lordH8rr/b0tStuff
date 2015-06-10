from twill.commands import *
from twill.extensions.check_links import check_links
from twill.extensions.require import no_require
import xml.etree.ElementTree as ET
import itertools
import re

def get_configurations():
	clear_cookies()
	
	tree 	     	= ET.parse('conf.xml')
	root 	     	= tree.getroot()
	publicregex 	= re.compile('.*public*.', re.IGNORECASE)
        adminSiteregex  = re.compile('.*admin*.', re.IGNORECASE) 
	sites        	= []	
	otherSites   	= []
	
	##########################	
	##Get info from xml conf##
	##########################
	for crawlusers in root.findall('User'):
		username = crawlusers.find('username').text
		password = crawlusers.find('password').text
	for crawlsites in root.findall('Sites'):
		ip = crawlsites.find('ip').text
	for sitetags in root.iter("site"):
		sites.append(sitetags.text)
	for admin_public in range(len(sites)):
		otherSites.append(re.findall(publicregex, sites[admin_public]))
		otherSites.append(re.findall(adminSiteregex, sites[admin_public]))
	
	#########################
	##remove empty elements##
	##flatten list of lists##
	#########################
	otherSites = filter(None, otherSites)
	flatListSites = itertools.chain(*otherSites)	
	old_sites = list(flatListSites)
	
	######################################
	##remove public and Admin from sites##
	##compare list and remove#############        
	######################################
	set1 = set(sites)
	set2 = set(old_sites)	
	newSites = list(set1 - set2)

	if newSites != None:
		createSites_signIn(newSites, ip, username, password)
	else:
		print 'No sites in config'
	
	if otherSites != None:
                for i in range(len(otherSites)):
                        APublic(otherSites[i], username, password, ip)
	else:
                print 'No Admin or Public sites in config'

def APublic(otherSites, usr, pwd, ip):
	baseSite = ip + ''.join(otherSites[0])
	newSite = ip + ''.join(otherSites[0]) + '/AsiCommon/Controls/Shared/FormsAuthentication/Login.aspx' #go to logon screen
        print newSite
	clear_cookies()
	go(newSite)
        showforms()
	fv("1", "ctl00_TemplateBody_Login1_LoginView1_Login1_UserName", usr)
        fv("1", "ctl00_TemplateBody_Login1_LoginView1_Login1_Password", pwd)
        submit()
	go(baseSite)
        check_links()
        print('Done with %s\n'% baseSite)

def createSites_signIn(sites, ip, usr, passwd):
	#Create Sign-in pages
	vroot = []
	vrootregex = re.compile('^(.*[\\\/])[^\\\/]*$')
	
	for x in range(len(sites)):
        	vroot.append(re.findall(vrootregex, sites[x]))
		
	defaultStaffSignin = ip + ''.join(vroot[0]) + 'iCore/Contacts/Staff_Sign_In.aspx'
	clear_cookies()
	go(defaultStaffSignin)
	get_input_fields(defaultStaffSignin)
	username_input = get_input_fields.username_input
	password_input = get_input_fields.password_input
	submit()
	fv("1", username_input, usr)
	fv("1", password_input, passwd)
	submit()
	redirect_output("visited.txt")
	showforms()
	#create sites here
	for i in range(len(sites)):
                sites[i] = ip + ''.join(sites[i])

	crawlSites(sites)

def crawlSites(sites):
	for i in range(len(sites)):
        	print sites[i]
		go(sites[i])
		check_links()
		print('Done with %s\n' % sites[i])

def get_input_fields(pagesource):
	submit()
        save_html("homepage.txt")
        regex1 = re.compile(".*input name=\S*")
        pagefile = open("homepage.txt", 'r')
        input_fields = re.findall(regex1, pagefile.read())
        print input_fields

        remove_junk_search = [s for s,x in enumerate(input_fields) if 'div' in x]
        for i in remove_junk_search:
                del input_fields[i]
        remove_junk_lastClicked = [l for l,y in enumerate(input_fields) if 'lastClicked' in y]
        for d in remove_junk_lastClicked:
                del input_fields[d]

        get_input_fields.username_input = re.findall(r'\"(.+?)\"', input_fields[0])
        get_input_fields.username_input = ''.join(get_input_fields.username_input)

        get_input_fields.password_input = re.findall(r'\"(.+?)\"', input_fields[1])
        get_input_fields.password_input = ''.join(get_input_fields.password_input)
			

get_configurations()
