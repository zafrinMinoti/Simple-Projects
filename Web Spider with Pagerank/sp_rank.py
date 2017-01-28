import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

# How many pages retrived total
	#	each page current rank is 1.0
	#	sum of all rank = number of pages retrived
cur.execute('SELECT COUNT(html) FROM Pages')
html_count = float(cur.fetchone()[0])
print 'Pages Retrived: ', html_count

# Total number of conncetion (pairs of pages)
cur.execute('SELECT COUNT(from_id) FROM Links')
count_union = cur.fetchone()[0]
print 'Total number of conncetions: ', count_union

#How many form Id and to id exists in Links Table
#Note that everything is not retrived, so this umber is going to be different
# cur.execute('SELECT COUNT(DISTINCT from_id) FROM Links')
# count_from_id = cur.fetchone()[0]
# cur.execute('SELECT COUNT(DISTINCT to_id) FROM Links')
# count_to_id = cur.fetchone()[0]
# print 'From ID Count / To ID Count: ', count_from_id, '/', count_to_id

# Home many links does each page have (outbound links)
	#	farction (%) of total number of connections
# outbound links is not importent due to equal number of outbound links on each page
# cur.execute('SELECT DISTINCT from_id FROM Links')
# ufrom_id = cur.fetchall()
# print type(ufrom_id)
# print '10 Unique from id', ufrom_id[:10]

# for i, j in enumerate(ufrom_id):
#     cur.execute('SELECT COUNT(to_id) FROM Links WHERE from_id = ?', (j[0],))
#     outbound_links = cur.fetchall()[0][0]
    # print outbound_links

# for i in ufrom_id:
#     cur.execute('SELECT COUNT(to_id) FROM Links WHERE from_id = ?', (ufrom_id[i],))
#     outbound_links = cur.fetchall()
#     print 'url ', j[0], ' has ', outbound_links, ' outbound links '


# How many links point to each page (inbound links)
	#	farction (%) of total number of connections

# get initial rank from inbound links counts
cur.execute('SELECT id FROM Pages WHERE html IS NOT NULL AND old_rank IS NULL')
urls_to_rank_1st = cur.fetchall()
# print 'new', urls_to_rank_1st

for i, j in enumerate(urls_to_rank_1st):
    current_id = j[0]
    cur.execute('SELECT COUNT(from_id) FROM Links WHERE to_id = ?', (current_id,))
    ilink_count = cur.fetchone()[0]
    # print ilink_count
    # print ilink_count/html_count*100
    new_rank = ilink_count/html_count
    cur.execute('UPDATE Pages SET old_rank = ?, new_rank = ? WHERE id = ?', (1, new_rank, current_id))
    conn.commit()


#When the initial rank already exists --
cur.execute('SELECT id FROM Pages WHERE html IS NOT NULL AND old_rank IS NOT NULL')
urls_to_rank = cur.fetchall()

for i,j in enumerate(urls_to_rank):
    current_id = j[0]
    cur.execute('SELECT from_id FROM Links Where to_id = ?', (current_id,))
    ib_links = cur.fetchall()
    ib_list = list()
    for y, z in enumerate(ib_links):
        cur.execute('SELECT new_rank FROM Pages WHERE id = ?', (z[0],))
        item_rank = cur.fetchone()[0]
        ib_list.append(item_rank)
    try: new_rank = sum(ib_list)/len(ib_list)
    except: continue
    cur.execute('SELECT new_rank FROM Pages WHERE id = ?', (current_id,))
    old_rank = cur.fetchone()[0]
    cur.execute('UPDATE Pages SET old_rank = ?, new_rank = ? WHERE id = ?', (old_rank, new_rank, current_id))
    conn.commit()


################### OLD CODE FOR TESTING ################
# inbound_links_data = dict()
# cur.execute('SELECT DISTINCT to_id FROM Links')
# uto_id = cur.fetchall()
# print 'Unique to id', uto_id[:10]

## for i, j in enumerate(uto_id):
##     cur.execute('SELECT COUNT(from_id) FROM Links WHERE to_id = ?', (j[0],))
##     inbound_links = cur.fetchall()[0][0]
##     # print inbound_links
##     print 'url ', j[0], ' has ', inbound_links, ' inbound links ', ' Rank: ', inbound_links/html_count*100


# for i, j in enumerate(uto_id):
#     cur.execute('SELECT from_id FROM Links WHERE to_id = ?', (j[0],))
#     inbound_links = cur.fetchall()
#     # print inbound_links
#     lst = []
#     for y, z in enumerate(inbound_links):
#         lst.append(z[0])
#     # print lst
#     inbound_links_data.update({j[0]:lst})
# #     print 'url ', j[0], ' has ', inbound_links, ' inbound links ', ' Rank: ', inbound_links/html_count*100
# # print inbound_links_data
# print len(inbound_links_data[5757])


# Waited average (avg1) => initial relative page rank score
	#	outbound * .2 + inbound * .8
#ratio = inbound_links/count_union

# adjusted weight (avg2)- inbound and outbound from/to good/bad pages
	#	avg1 of all outbound links * .2 + avg1 of all inbound * .8

# Get the average of each inbound link source
# in_link_source_score = dict()
# for k, v in inbound_links_data:

    # in_link_source_score.update({k:})

conn.close()
