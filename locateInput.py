import re
from twill.commands import *


def get_price_fields(url):
	go(url)
	showforms()
	removeTmpFile = save_html("tmpfile.txt")
	regex1 = re.compile(".*input name=\S*")
        pagefile = open("tmpfile.txt", 'r')
        input_fields = re.findall(regex1, pagefile.read())
        FindFields = [s for s,x in enumerate(input_fields) if 'Override' in x]
	for i in FindFields:
                override = input_fields[i]
	override = override.strip()
	print override
	override = re.findall(r'\"(.+?)\"', override)
	print override
	return override

