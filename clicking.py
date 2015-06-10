from selenium import webdriver
import re

def click(CommonItemUrl):

	driver = webdriver.Firefox()
	driver.get(CommonItemUrl)
	driver.find_element_by_id("ctl00_TemplateBody_WebPartManager1_gwpciGeneralProductDisplay_ciGeneralProductDisplay_DynamicProductDisplay_AddToCart").click()
	driver.close()

