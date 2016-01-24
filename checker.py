from bs4 import BeautifulSoup as soup
import string
import urllib2
import re

# Generates usernames with a higher weightage for more probable usernames
def username_generator(first_name, last_name, middle_name=None, linkedin_url=None, angellist_url=None, twitter_url=None):
	usernames = dict()
	username_chars = set([char for char in string.ascii_lowercase] + [str(i) for i in range(10)] + ['_', '-', '.'])

	# Adds usernames to the username set
	def add_username(username):
		if username in usernames:
			usernames[username] += 1
		else:
			usernames[username] = 1

	# Extracts usernames from URLs
	def extract_username(url, stub):
		url = url.lower()
		if stub in url:
			start = url.index(stub) + len(stub)
			end = start
			while end in username_chars:
				end += 1

			username = url[start:end + 1]
			add_username(username)

	for url in [(linkedin_url, 'linkedin.com/in/'), (angellist_url, 'angel.co/'), (twitter_url, 'twitter.com/')]:
		if url[0]:
			extract_username(url[0], url[1])

	# Common usernames
	add_username(first_name + last_name)
	add_username(first_name[0] + last_name)
	add_username(first_name + last_name[0])
	add_username(first_name + '_' + last_name)
	add_username(first_name[0] + '_' + last_name)
	add_username(first_name + '_' + last_name[0])
	add_username(first_name + '_' + last_name[0])
	add_username(first_name + '.' + last_name)
	add_username(first_name[0] + '.' + last_name)
	add_username(first_name + '.' + last_name[0])
	add_username(first_name + '.' + last_name[0])

	if middle_name:
		add_username(first_name + middle_name + last_name)
		add_username(first_name + middle_name[0] + last_name)
		add_username(first_name[0] + middle_name + last_name)
		add_username(first_name[0] + middle_name[0] + last_name)
		add_username(first_name + middle_name + last_name[0])
		add_username(first_name + middle_name[0] + last_name[0])
		add_username(first_name + '_' + middle_name + '_' + last_name)
		add_username(first_name + '_' + middle_name[0] + '_' + last_name)
		add_username(first_name[0] + '_' + middle_name + '_' + last_name)
		add_username(first_name[0] + '_' + middle_name[0] + '_' + last_name)
		add_username(first_name + '.' + middle_name + '.' + last_name)
		add_username(first_name + '.' + middle_name[0] + '.' + last_name)
		add_username(first_name[0] + '.' + middle_name + '.' + last_name)
		add_username(first_name[0] + '.' + middle_name[0] + '.' + last_name)

	# TODO
	def username_weighter():
		pass

def email_generator(usernames, domains):
	emails = dict()

	# Finds any emails in domain source code
	def parse_HTML(html):
		s = soup(html)
		for string in s.strings:
			match = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string)
			if match:
				emails[match.group(0)] = 1
		for email in s.select('a[href^=mailto]'):
			emails[email.string] = 1

	for domain in domains:
		if domain[:4] != 'http':
			domain = 'http://' + domain
		# Might not have permission to scrape
		try:
			resp = urllib2.urlopen(domain).read()
			parse_HTML(resp)
		except:
			pass

