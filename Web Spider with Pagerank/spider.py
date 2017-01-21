import sqlite3, urllib
from bs4 import *

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

#Only use this to start over
cur.executescript('''
	DROP TABLE IF EXISTS Pages;
	DROP TABLE IF EXISTS Links;
	DROP TABLE IF EXISTS Webs;
	''')

#Create the database - Only executed the first time the program runs
cur.executescript('''
	CREATE TABLE IF NOT EXISTS Pages
		(id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT, error INTEGER, old_rank REAL, new_rank REAL);
	CREATE TABLE IF NOT EXISTS Links
		(from_id INTEGER, to_id INTEGER);
	CREATE TABLE IF NOT EXISTS Webs
		(url TEXT UNIQUE);
	''')

root = 'http://python-data.dr-chuck.net/' #to be used for enternal links where http:// is absent

#Limiting the number of pages to be retives to control run-time and disk space
link_count = int(raw_input('How many pages would you like to retrive?\n>> '))

while link_count > 0: 
	#The program a re-startable. So First check if it is already in progress
	cur.execute('SELECT id, url FROM Pages WHERE html is NULL ORDER BY RANDOM() LIMIT 1')
	row = cur.fetchone()

	if row is not None:
		row = row[1]
		print '\n\n\nSELECTED URL: ', row
		start_url = row.encode('utf-8')

		html = urllib.urlopen(row).read()
		cur.execute('UPDATE Pages SET html=? WHERE url=?', (html, start_url))
		conn.commit()
		print '\nRetrived... ', row, '\n'
		link_count -=1
		
		# #Persing the html to get <a> tags
		# bs = BeautifulSoup(html, "lxml")
		# atags = bs('a')
		# for tag in atags:
		# 	url = tag.get('href', None)

		# 	#Saving urls in the database to be retrived later
		# 	cur.execute('INSERT OR IGNORE INTO Pages(url, new_rank) VALUES (?,?)', (url, 1.0))
		# 	conn.commit()
		# 	print 'Saving to be retrived', url

		# 	#Insert data into Links table to show who is connected to who - form_id & to_id
		# 	cur.execute('SELECT id FROM Pages WHERE url =?', (url, ))
		# 	to_id = cur.fetchone()[0]
		# 	cur.execute('INSERT INTO Links(from_id, to_id) VALUES (?,?)', (encoded_row, url.encode('utf-8')))
		# 	conn.commit()

	else:
		# Start the program for the first time
		start_url = raw_input('Enter a Start URL:\n>>')
		if len(start_url) < 1: start_url = root

		print '\n\n\nTrying to retrived... ', start_url
		html = urllib.urlopen(start_url).read()
		cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (start_url, ))
		cur.execute('INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES (?,?,?)', (start_url, html, 1.0))
		conn.commit()
		print '\nRetrived...', start_url, '\n'
		link_count -= 1

	#Get form id:
	cur.execute('SELECT id FROM Pages WHERE url=?', (start_url, ))
	from_id = cur.fetchone()[0]

	#Persing the html to get <a> tags
	bs = BeautifulSoup(html, "lxml")
	atags = bs('a')
	for tag in atags:
		raw_link = tag.get('href', None)

		#Error check
		if raw_link.startswith('http') : url = raw_link
		else: url = root+raw_link
		if url.endswith('/') : url = url[:-1]
		if not url.endswith('.html') or url.endswith('.htm'):
			#cur.execute('INSERT OR IGNORE INTO Pages(url, error) VALUES (?,?)', (url, -1))
			#conn.commit()
			print '\nERROR recorded with...', url, '\n'
			continue
			
		else:
			#Saving urls in the database to be retrived later
			cur.execute('INSERT OR IGNORE INTO Pages(url, new_rank) VALUES (?,?)', (url, 1.0))
			conn.commit()
			print 'Saving to be retrived', url

			#Insert data into Links table to show who is connected to who - form_id & to_id
			cur.execute('SELECT id FROM Pages WHERE url =?', (url, ))
			to_id = cur.fetchone()[0]
			cur.execute('INSERT INTO Links(from_id, to_id) VALUES (?,?)', (from_id, to_id))
			conn.commit()

conn.close()
