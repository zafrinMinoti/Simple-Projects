import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

# How many pages retrived total
	#	each page current rank is 1.0
	#	sum of all rank = number of pages retrived
cur.execute('SELECT COUNT(html) FROM Pages')
count_html = float(cur.fetchone()[0])
print 'Pages Retrived: ', count_html

# Total number of conncetion (pairs of pages)
cur.execute('SELECT COUNT(from_id) FROM Links')
count_links = cur.fetchone()[0]
print 'Total number of conncetions: ', count_links

#How many form Id and to id exists in Links Table
#Note that everything is not retrived, so this umber is going to be different
cur.execute('SELECT COUNT(DISTINCT from_id) FROM Links')
count_from_id = cur.fetchone()[0]

cur.execute('SELECT COUNT(DISTINCT to_id) FROM Links')
count_to_id = cur.fetchone()[0]

print 'From ID Count / To ID Count: ', count_from_id, '/', count_to_id

# Home many links does each page have (outbound links)
	#	farction (%) of total number of connections
cur.execute('SELECT DISTINCT from_id FROM Links')
ufrom_id = cur.fetchall()
print type(ufrom_id)
print 'Unique from id', ufrom_id[:10]

# for i, j in enumerate(ufrom_id):
#     cur.execute('SELECT COUNT(to_id) FROM Links WHERE from_id = ?', (j[0],))
#     outbound_links = cur.fetchall()[0][0]
    #print outbound_links
	
###### DID NOT WORK ######
# for i in ufrom_id:
#     cur.execute('SELECT COUNT(to_id) FROM Links WHERE from_id = ?', (ufrom_id[i],))
#     outbound_links = cur.fetchall()
#     print outbound_links

# for id in ufrom_id:
# 	cur.execute('SELECT COUNT(to_id) FROM Links WHERE from_id = ?', (id, ))
# 	outbound_links = cur.fetchall()
# 	print id, group_from_id
###### DID NOT WORK ###### END ######


# How many links point to each page (inbound links)
	#	farction (%) of total number of connections
cur.execute('SELECT DISTINCT to_id FROM Links')
uto_id = cur.fetchall()
print 'Unique to id', uto_id[:10]

for i, j in enumerate(uto_id):
    cur.execute('SELECT COUNT(from_id) FROM Links WHERE to_id = ?', (j[0],))
    inbound_links = float(cur.fetchall()[0][0])
    print inbound_links, inbound_links/count_html*100


# Waited average (avg1) => initial relative page rank score
	#	outbound * .2 + inbound * .8
#ratio = inbound_links/count_links

# adjusted weight (avg2)- inbound and outbound from/to good/bad pages
	#	avg1 of all outbound links * .2 + avg1 of all inbound * .8

conn.close()
