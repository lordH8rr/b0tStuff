from twill.commands import *
import xml.etree.ElementTree as ET
import re
import os
import errno
import timeit
import thread
import random
import clicking
import locateInput
import Items


class shoppingUser:
	IsStaff = False
	ContShop = False
	numOfItems = None
	IP = None
	uid = None
	pwd = None

class item:
	quantity = None
	price = None
	Donation = 'imis/MBR/Donate/iCore/Fundraising/Donate_Now.aspx'
	Membership = 'iMIS/iCore/Contacts/ContactLayouts/AccountPage.aspx'
	CommonItem = 'imis/MBR/Shop/iCore/Store/StoreLayouts/Store_Home.aspx'
	CurrentItem = None
	itemType = [Membership, Donation, CommonItem]

        		
def get_current_site():
	redirect_output("tmpfile.txt")
	info()
	reset_output()
	getsite = re.compile("http:\/\/.*")
	currentSite = open("tmpfile.txt", "r") 
	sitearry = re.findall(getsite, currentSite.read())
	site = str(sitearry[0])
	print site
	removeTmpFile()
	return site


def removeTmpFile():
	try:
		os.remove("tmpfile.txt")
	except OSError:
		pass	


def BuyOne(usrItem, usrCred):
	usrItem.CommonItem = usrCred.IP + usrItem.CommonItem
	go(usrItem.CommonItem)
	Items = ItemSelect(usrItem.CommonItem)
	print Items
	ItemIndex = len(Items)
	chozenItem = random.randint(0, ItemIndex)
	CurrentItem = Items[chozenItem]
	CurrentItem = CurrentItem.strip()
	print CurrentItem
	follow(str(CurrentItem))	
	#get current site
	usrItem.CurrentItem = get_current_site()
	
	if(usrCred.IsStaff == True):
		#locate Price overrideField
		override = locateInput.get_price_fields(usrItem.CurrentItem)			
		fv("1", override, usrItem.price)
	else:
		#send url
		go(item)
	
	#add to cart clicking.py
	clicker()
	



#def BuyMulti(usrItem):
#	go(usrItem.CommonItem)
#       follow('') #random from 10-20
#	if(usrItem.IsStaff == True):
#		find price input field
#                fv("1", "#inputform", usrItem.price)




def ItemSelect(ItemPage):
	redirect_output("ItemPage.txt")
	showlinks()
	reset_output()
	itemList = Items.getItemList()
 	
	print('number of Items: %i ' % len(itemList))	
	
	return itemList	




def Staff(Usr):
	IPSignIn = Usr.IP + 'iMIS/iCore/Contacts/Staff_Sign_In.aspx'
	print IPSignIn
	usr = Usr.uid
	passwd = Usr.pwd
	print usr
	print passwd
	go(IPSignIn)
	submit()
	showforms()
	get_input_fields(IPSignIn)
	username_input = get_input_fields.username_input
        password_input = get_input_fields.password_input
	fv("1", username_input, usr)
        fv("1", password_input, passwd)
        submit()
	showforms()
#	Buy one item, set price
	staffItem = item()
	staffItem.price = random.uniform(20.0, 101.7)
	BuyOne(staffItem, Usr)
	
	
#	Buying Multi , set price
#	staffItem.price = random.uniform(20.0, 101.7)
#	staffItem.ContinueShopping == True	
#	BuyMulti(staffItem, usr)
	


def Mbr(Usr, IP, uid, pwd):
	IPSignIn = IP + 'iMIS/iCore/Contacts/Sign_In.aspx'
        IPBase = IP + 'iMIS/Mbr' 
        go(IP)
        submit()
        showforms()
        get_input_fields(IP)
        username_input = get_input_fields.username_input
        password_input = get_input_fields.password_input
        fv("1", username_input, "jphelps")
        fv("1", password_input, "jphelps1")
        submit()
	
	#set item types

        #start adding items

        #decrement the number of items
        #display current item number

        #show completion message



def get_input_fields(pagesource):
	save_html("tmpfile.txt")
	regex1 = re.compile(".*input name=\S*")
        pagefile = open("tmpfile.txt", 'r')
        input_fields = re.findall(regex1, pagefile.read())
        print input_fields
	removeTmpFile()

        remove_junk_search = [s for s,x in enumerate(input_fields) if 'div' in x]
        for i in remove_junk_search:
                del input_fields[i]

        remove_junk_lastClicked = [l for l,y in enumerate(input_fields) if 'lastClicked' in y]
        for d in remove_junk_lastClicked:
                del input_fields[d]

 	#find username field
        get_input_fields.username_input = re.findall(r'\"(.+?)\"', input_fields[0])
        get_input_fields.username_input = ''.join(get_input_fields.username_input)

	#find password field
        get_input_fields.password_input = re.findall(r'\"(.+?)\"', input_fields[1])
        get_input_fields.password_input = ''.join(get_input_fields.password_input)

	print get_input_fields
	

def login():
	clear_cookies()
	
	tree = ET.parse('conf.xml')
	root = tree.getroot()
	
	for crawlusers in root.findall('userdata'):
		uid = crawlusers.find('username').text
		pwd = crawlusers.find('password').text
		print uid
		print pwd

	for crawlsites in root.findall('Site'):
		url = crawlsites.find('IP').text
	

	
	##Users that will shop##
	PublicUsr = shoppingUser()
	PublicUsr.IsStaff = False
	PublicUsr.numOfItems = 10
	PublicUsr.IP = url
	PublicUsr.uid = uid
	PublicUsr.pwd = pwd

	StaffUsr = shoppingUser()
	StaffUsr.IsStaff = True
	StaffUsr.numOfItems = 10
	StaffUsr.IP = url
	StaffUsr.uid = uid
	StaffUsr.pwd = pwd

	PublicUsrOneItem = shoppingUser()
	PublicUsrOneItem.IsStaff = False
	PublicUsrOneItem.numOfItems = 1
	PublicUsrOneItem.IP = url
	PublicUsrOneItem.uid = uid 
	PublicUsrOneItem.pwd = pwd


	StaffUsrOneItem = shoppingUser()
	StaffUsrOneItem.IsStaff = True
	StaffUsrOneItem.numOfItems = 1
	StaffUsrOneItem.IP = url
	StaffUsrOneItem.uid = uid
	StaffUsrOneItem.pwd = pwd



	try:
#        	thread.start_new_thread( Mbr, (PublicUsr) )
#        	thread.start_new_thread( Mbr, (StaffUsr) )
#        	thread.start_new_thread( Staff, (StaffUsr, ) )
#		thread.start_new_thread( Mbr, (PublicUsrOneItem) )
#		thread.start_new_thread( Mbr, (StaffUsrOneItem) )
		thread.start_new_thread( Staff, (StaffUsrOneItem, ) )
	
	except:
        	print "Could not start"
	
	while 1:
        	pass

login()	
