import re
import itertools
from bs4 import BeautifulSoup
import requests
import urllib.parse
import random
from lxml import etree
import lxml.html
from selenium import webdriver
from sys import stdout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import argparse

url = ""

results = set()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def inject(injection, browser):
	browser.get(url + injection)
	try:
		WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for alerts to appear')
		alert = browser.switch_to.alert
		alert.accept()
		print(bcolors.FAIL + "XSS" + " for " + injection + bcolors.ENDC)
		results.add(injection)
	except TimeoutException:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC + " for "+ injection)

def scan():
	browser = webdriver.Firefox()
	browser.get(url)
	print("Scanning: " + url)
	print("=" * 60)
	check_headers()

	file = open("xss.txt","r")
	print("=" * 60)
	print("Testing predefined patterns: xss.txt + mutations\n")
	for injection in file:
		if injection != "":
			injection_transformations = generate_transformations(injection[:-1])
			for xss in injection_transformations:
				inject(xss, browser)
	browser.quit()
	print("")

	print("=" * 60)
	print("Possible XSS Vulnerabilities:\n")
	for result in results:
		print(result)

def charToHex(c):
	return "\\x" + format(ord(c), "x")

def charToUnicodeHex(c):
	return "&#" + format(ord(c), "x") + ";"

def encode_hex(injection):
	result = ""
	for c in injection:
		result += charToHex(c)
	return result

def encode_unicode_hex(injection):
	result = ""
	for c in injection:
		result += charToUnicodeHex(c)
	return result

def randomUpperLower(c):
	if random.randint(0,2) == 1:
		return c.lower()
	else:
		return c.upper()

def randomizeUpperLower(injection):
	result = ""
	for c in injection:
		result += randomUpperLower(c)
	return result

def allUpper(injection):
	return injection.upper()

def encode_url(input):
	return urllib.parse.quote(input, safe='')

def generate_transformations(injection):
	injection_transformations = [injection,
                encode_url(injection),
                encode_url(encode_url(injection)),
		randomizeUpperLower(injection),
		allUpper(injection)]
	return injection_transformations

def check_headers():
	useragentheader = 'thisismysupersecretuseragent'
	fromheader = "thisismysupersecretfromheader"
	headers = {
    	'User-Agent': useragentheader,
    	'From': fromheader
		}
	r = requests.get(url + "abc")
	if useragentheader.lower() in r.text.lower():
		print(bcolors.WARNING + "Warning" + bcolors.ENDC + "\tUser-Agent found in html")
	else:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC + "\tUser-Agent not found in html")
	if fromheader.lower() in r.text.lower():
		print(bcolors.WARNING + "Warning" + bcolors.ENDC + "\tFrom-Header found in html.")
	else:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC + "\tFrom-Header mot found in html")


# Create the parser
my_parser = argparse.ArgumentParser(description='Scan a website for xss by instrumenting seleium browsers.')

# Add the arguments
my_parser.add_argument('URL',
                       metavar='url',
                       type=str,
                       help='URL to the parameter')

# Execute the parse_args() method
args = my_parser.parse_args()

url = args.URL
scan()
