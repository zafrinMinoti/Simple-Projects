import sqlite3

conn = sqlite3.connect('spider.sqlite')
curr = conn.cursor()

print 'THIS WILL DELETE ALL DATA FROM spider.sqlite'
delete = raw_input('Are you sure? Type "YES" to continue reseting\n\t>>')

if delete == 'YES'
	cur.executescript('''
		DROP TABLE IF EXISTS Pages;
		DROP TABLE IF EXISTS Links;
		DROP TABLE IF EXISTS Webs;
		''')
	cur.commit()

else: 
	print "oh boy, you got me scared there!"
	
conn.close()
quit()
