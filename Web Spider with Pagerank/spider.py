import urllib, sqlite3
from bs4 import *

root = "http://python-data.dr-chuck.net/"
conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS Pages;
	DROP TABLE IF EXISTS Links;
	DROP TABLE IF EXISTS Webs;
	''')

cur.executescript('''
	CREATE TABLE IF NOT EXISTS Pages
		(id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT, error INTEGER, old_rank REAL, new_rank REAL);
	CREATE TABLE IF NOT EXISTS Links
		(from_id INTEGER, to_id INTEGER);
	CREATE TABLE IF NOT EXISTS Webs
		(url TEXT UNIQUE);
	''')



link_count = int(raw_input('How many pages would you like to retrive?\n>> '))

while link_count > 0:
	#Check if we are already in progress
	cur.execute('SELECT url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
	row = cur.fetchone()
	print 'cur.fetchone()', cur.fetchone()
	print 'row', row

	if row is not None: # if data retraval is in progress
		start_url = row
		print '\n\nstarting with url: ', start_url 
		try:
			html = urllib.urlopen(start_url).html
			print 'Retriving', start_url, '\n'
			cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (start_url, ))
			cur.execute('UPDATE Pages SET html=? WHERE url =?', (html, start_url))
			conn.commit()

			bs = BeautifulSoup(html, "lxml")
			atags = bs('a')
			for tag in atags:
				url = tag.get('href', None)
				print 'Saving to be retrived', url
				cur.execute('INSERT OR IGNORE INTO Pages(url) VALUES (?)', (url, ))
				conn.commit()

		except: 
			cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (start_url, ) )
			conn.commit()
			print 'SOMETHING FAILED with the url picked from the database'


	else:
		#Starting the program for the first time
		start_url = raw_input('Enter a Start URL:\n>>')
		if len(start_url) < 1: start_url = 'http://python-data.dr-chuck.net'

		try:
			html = urllib.urlopen(start_url).read()
			print 'Retriving', start_url, '\n'
			cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (start_url, ))
			cur.execute('INSERT OR IGNORE INTO Pages(url, html) VALUES (?, ?)', (start_url, html))
			conn.commit()

			bs = BeautifulSoup(html, "lxml")
			atags= bs('a')

			count = 0
			for tag in atags:
				url = root+str(tag.get('href', None))
				url = url.encode('utf-8')
				print 'URLLLLLL: ', url
				###################################
				###################################
				#above code - produces unicode
				#################################
				###################################
				
				if not url.endswith('html') or url.endswith('htm'): 
					print 'skipping', url
					continue
				print 'Saving to be retrived', url
				count += 1
				print count
				cur.execute('INSERT OR IGNORE INTO Pages(url) VALUES (?)', (url, ))
				conn.commit()

		except: 
			cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (start_url, ) )
			conn.commit()
			print 'SOMETHING FAILED with start url'
	link_count -=1
