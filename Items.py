import re
import os

def getItemList():
	
	regItems = re.compile("(?<=. )(.*)(?=.=>)")
	pagefile = open("ItemPage.txt", "r")
	ItemList = re.findall(regItems, pagefile.read())
	os.remove("ItemPage.txt")
	#remove white space from elements
	ItemList = filter(lambda Links: Links.strip(), ItemList)	
	#print ItemList
	del ItemList[0:57]
	del ItemList[25:]
	#print ItemList
	#print [i for i, x in enumerate(ItemList) if x == 'Events ']
	return ItemList	

