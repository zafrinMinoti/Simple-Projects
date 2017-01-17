''' This program generates random password
Save the password in database
'''
#Author: Zafrin Minoti
#Simple Project
#Date: 1/10/17 - 1/12/17

import random
import string

bananas = True

def gen_pswd():
	''' Generate a password at least 8 characters long
	that starts with a letter ensures to contains numbers
	and special characters(for difficult level password only)
	length of password varies 
	'''
	stringlist_1st = []
	stringlist = []
	for i in range(random.randint(1,2)):
		stringlist_1st.append(random.choice(string.ascii_letters))
	for i in range(random.randint(1,2)):
		stringlist.append(random.choice(string.ascii_uppercase))
	for i in range(random.randint(1,2)):
		stringlist.append(random.choice(string.ascii_lowercase))
	for i in range(random.randint(2,4)):
		stringlist.append(str(random.randint(0,9)))
	if sp_char =='y':
		for i in range(random.randint(2,3)):
			stringlist.append(random.choice(string.punctuation))

	random.shuffle(stringlist)
	pswd = "".join(stringlist_1st)+"".join(stringlist)
	
	if len(pswd) < 8:
		for i in range(random.randint(8,10)-len(pswd)):
			extra_char = random.choice(characters)
			pswd = pswd[0:1]+extra_char+pswd[1:]

	return pswd
#
while bananas:
	sp_char = raw_input('\nDo you want to include special characters?\n(Y/N?)\n>> ').lower()

	#get the password or give helpful error message
	if sp_char == 'n':
		characters = string.ascii_letters+str(string.digits)
		pswd = gen_pswd()
		print 'Your AWESOME random password: ' + pswd

	elif sp_char == 'y':
		characters = string.ascii_letters+str(string.digits)+string.punctuation
		pswd = gen_pswd()
		print 'Your AWESOME random password: ' + pswd

	else: 
		print 'Sorry, you have an invalid input. Please try again.\n'
		quit()

	#Viwe details about the password, if wanted
	details = raw_input('\nWould you like to see details about your password?\n(Y/N?)\n>> ').lower()
	if details == 'y':
		caps = string.ascii_lowercase
		small = string.ascii_uppercase
		numb = string.digits
		sp = string.punctuation

		def count(char_type,pswd_method):
			''' Returens how many character of a single type exists in a random password '''
			char_type_count = 0
			for char in pswd_method:
				if char in char_type:
					char_type_count +=1
			return char_type_count

		print 'Uppercase: ', count(caps,pswd)
		print 'Smallcase: ', count(small,pswd)
		print 'Numbers: ', count(numb,pswd)
		print 'Special Characters: ', count(sp,pswd)
		print '\nLength: ', len(pswd)

	rerun = raw_input('\nWould you like to generate another password?\n(Y/N)\n>> ').lower()
	if rerun == 'n': 
		bananas = False

save = raw_input('\nWould you like to save the password?\n(Y/N?))\n>> ').lower()

if save == 'n': quit()


#make connection to database and create tables
import sqlite3
conn = sqlite3.connect('accounts.sqlite')
cur = conn.cursor()
cur.executescript('''
	CREATE TABLE IF NOT EXISTS AccountTypes
		(id INTEGER PRIMARY KEY, type TEXT UNIQUE);
	CREATE TABLE IF NOT EXISTS Emails
		(id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL);
	CREATE TABLE IF NOT EXISTS Accounts
		(id INTEGER PRIMARY KEY, name TEXT, company TEXT,
		type_id INTEGER, accNumber INTEGER, link TEXT,
		email_id INTEGER, username TEXT, password TEXT, dueDate INTEGER,
		FOREIGN KEY (type_id) REFERENCES AccountTypes(id),
		FOREIGN KEY (email_id) REFERENCES Emails(id))
	''')

#Ask different account information for which the password was generated
print '\nFirst add your account information. Press enter if not applicable.\n'
name = raw_input('Account Name: ')
link = raw_input('Login Link: ')
username = raw_input('Username: ')

company = raw_input('Company Name: ')
email = raw_input('Email: ')
acc_type = raw_input('Account Type: ')
accNumber = raw_input('Account Number: ')
dueDate = raw_input('Due Date (only date of the month): ')

#Save password and other information into the database
cur.execute('INSERT OR IGNORE INTO AccountTypes (type) VALUES (?)', (acc_type, ))
cur.execute('INSERT OR IGNORE INTO Emails (email) VALUES (?)', (email, ))

cur.execute('SELECT id FROM Emails WHERE email=(?)', (email, ))
last_email = cur.fetchone()[0]
cur.execute('SELECT id FROM AccountTypes WHERE type=?', (acc_type, ))
last_accType = cur.fetchone()[0]

cur.execute(
	'''INSERT INTO Accounts 
	(name, link, username, password, company, accNumber, dueDate, email_id, type_id) 
	VALUES ( ?,?,?,?,?,?,?,?,? )''',
	(name, link, username, pswd, company, accNumber, dueDate, last_email, last_accType))

conn.commit()
conn.close()