import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

print 'THIS WILL SET ALL RANKS to 1.0 at spider.sqlite'
reset = raw_input('Are you sure? Type "YES" to continue reseting\n\t>> ')

if reset == 'YES':
	cur.execute('UPDATE Pages SET old_rank = NULL, new_rank = 1.0')
	conn.commit()

else:
	print "oh boy, you got me scared there!"

conn.close()
