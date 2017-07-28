from urllib.request import *
import os
import time
import math
import re
import sys
from bs4 import BeautifulSoup

def createUserDirectory(userName):
	if not (os.path.exists(userName)):
		os.makedirs(userName)

def fileExtension(data):
	matchpy = re.search(r'input\([\w\s\S]*\)', data)
	if matchpy:
		return '.py'
	matchjava = re.search(r'public static void main', data)
	if matchjava:
		return '.java'
	matchcpp = re.search(r'<iostream>', data)
	if matchcpp:
		return '.cpp'
	matchc = re.search(r'<stdio.h>', data)
	if matchc:
		return '.c'

def write(data):
	fileExt = fileExtension(data)
	f = open(userName + '/' + solName + fileExt, 'w')
	f.write(data)
	f.close()

def solScrapper(url):
	createUserDirectory(userName)
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req).read()
	soup = BeautifulSoup(html, "lxml")
	li = soup.ol.findAll("div")
	lines = ""
	for i in range(0,len(li)):
		l = list(li[i].strings)
		lines += ''.join(l) + '\n'
	write(lines)
	currentTime2 = time.time()
	time1 = math.ceil(currentTime2 - currentTime1)	
	print("Fetched %s in %s seconds"%(solName, str(time1)))

def acceptedSolURLScrapper(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req).read()
	soup = BeautifulSoup(html, "lxml")
	table = soup.find("table", attrs={"class": "dataTable"})
	td = table.find("td", {'width': '75'})
	try:
		acceptedSolURL = 'https://www.codechef.com' + td.a['href']
		solScrapper(acceptedSolURL)
		global answers
		answers += 1
	except KeyError:
		print(solName + " couldn't be fetched")
		return

def allSolsNames():
	userUrl = 'https://www.codechef.com/users/'+ userName
	req = Request(userUrl, headers={'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req).read()
	soup = BeautifulSoup(html, "lxml")
	section = soup.find("section", attrs={"class" :"rating-data-section problems-solved"})
	aTags = section.findAll("a")
	aTagsToBeCrawled = []
	global currentTime1
	global solName
	baseUrl = "https://www.codechef.com"
	for i in range(len(aTags)):
		aTagsToBeCrawled.append(baseUrl + aTags[i]['href'])
		solName = aTags[i].string
		currentTime1 = time.time()
		acceptedSolURLScrapper(aTagsToBeCrawled[i])
	print("You've successfully fetched %d answers"%(answers))

print("----------/CodeChef Crawler/----------")
userName = input("Enter the username: ")
print("Answers are being fetched for %s...."%(userName))
answers = 0

allSolsNames()