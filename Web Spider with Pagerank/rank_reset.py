import sqlite3

conn = sqlite3.connect('spider.sqlite')
curr = conn.cursor()

print 'THIS WILL SET ALL RANKS to 1.0 at spider.sqlite'
reset = raw_input('Are you sure? Type "YES" to continue reseting\n\t>>')

if delete == 'YES'
	cur.execute('UPDATE Pages SET old_rank = 0, new_rank = 1.0')
	curr.commit()

else: 
	print "oh boy, you got me scared there!"

conn.close()
quit()
