import sqlite3, urllib
from bs4 import *

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

link_count = int(raw_input('How many pages would you like to retrive?\n>> '))
root = 'http://python-data.dr-chuck.net'

while link_count > 0:

	cur.execute('SELECT id, url FROM Pages WHERE html is NULL ORDER BY RANDOM() LIMIT 1')
	row = cur.fetchone()[1]

	if row is not None:
		print '\n\n\nSELECTED URL: ', row
		print 'initial type: ', type(row)

		encoded_row = row.encode('utf-8')
		# print 'selected url again... ', row
		# print 'type of row after encoding: ', type(row)
		# print 'encoded url... ', encoded_row
		# print 'type after encoding: ', type(encoded_row)

		link_count -=1
		html = urllib.urlopen(row).read()
		################################################################
		cur.execute('UPDATE Pages SET html=? WHERE url=?', (html, encoded_row))
		conn.commit()
		########### THIS # IS # THE # PROBLEM ##########
		################################################################
		print '\nRetrived... ', row
		#print html
		bs = BeautifulSoup(html, "lxml")
		atags = bs('a')
		for tag in atags:
			url = tag.get('href', None)
			print 'Saving to be retrived', url
			cur.execute('INSERT OR IGNORE INTO Pages(url, new_rank) VALUES (?,?)', (url, 1.0))
			conn.commit()
			cur.execute('SELECT id FROM Pages WHERE url =?', (url, ))
			to_id = cur.fetchone()[0]
			cur.execute('INSERT INTO Links(from_id, to_id) VALUES (?,?)', (encoded_row, url.encode('utf-8')))
			conn.commit()

	else:
		# Start the program for the first time
		start_url = raw_input('Enter a Start URL:\n>>')
		if len(start_url) < 1: start_url = root

		print '\n\n\nTrying to retrived... ', start_url
		html = urllib.urlopen(start_url).read()
		link_count -= 1
		cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (start_url, ))
		cur.execute('INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES (?,?,?)', (start_url, html, 1.0))
		conn.commit()
		print 'Retrived...', start_url


		bs = BeautifulSoup(html, "lxml")
		atags = bs('a')
		for tag in atags:
			raw_link = tag.get('href', None)
			if not raw_url.startswith('http') : url = root+raw_url
			else: url = raw_url
			if url.endswith('/') : url = url[:-1]
			if not url.endswith('htm') or url.endswith('html'):
				cur.execute('INSERT OR IGNORE INTO Pages(url, error) VALUES (?,?)', (url, -1))
				conn.commit()
				print '\nERROR recorded with...', url, '\n'
				continue
			cur.execute('INSERT OR IGNORE INTO Pages(url) VALUES (?)', (url, ))
			conn.commit()
			print 'Saving to be retrived', url 

conn.close()

