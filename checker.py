from bs4 import BeautifulSoup as soup
import string
import urllib2
import re

# Utility function that is called throughout program
def strip_domain(domain):
	start = 7
	if domain[4] == 's':
		if domain[8:11] == 'www':
			start = 12
		else:
			start = 8
	elif domain[7:10] == 'www':
		start = 11
	end = start
	while end < len(domain) and domain[end] != '/':
		end += 1
	return domain[start:end]

# Generates usernames with a higher weightage for more probable usernames
def username_generator(first_name, last_name, middle_name=None, domains=[], linkedin_url=None, angellist_url=None, twitter_url=None):
	usernames = dict()
	username_chars = set([char for char in string.ascii_lowercase] + [str(i) for i in range(10)] + ['_', '-', '.'])

	# Adds usernames to the username set
	def add_username(username):
		username = username.lower()
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
			while end < len(url) and url[end] in username_chars:
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
	add_username(first_name + '.' + last_name)
	add_username(first_name[0] + '.' + last_name)
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

	for domain in domains:
		stripped_domain = strip_domain(domain)
		add_username(stripped_domain[:stripped_domain.index('.')])

	def username_weight(username):
		letters = False
		numbers = False
		symbols = False
		num_strs = map(str, range(10))
		chars = set(username)
		for char in chars:
			if char in string.ascii_lowercase:
				letters = True
			elif char in num_strs:
				numbers = True
			else:
				symbols = True
		if letters:
			if numbers:
				if symbols:
					return 0.7 # letters, numbers, and symbols
				return 0.85 # letters and numbers
			elif symbols:
				return 0.85 # letters and symbols
			return 1.0 # letters only
		elif numbers:
			if symbols:
				return 0.2 # numbers and symbols
			return 0.3 # numbers only
		else:
			return 0.1 # symbols only

	for username in usernames:
		first = usernames[username]
		usernames[username] *= username_weight(username)
		print username, 'first has weight', first, 'now has weight', username_weight(username), 'resulting in', usernames[username]

	return usernames
		
# Generates potential email addresses
def email_generator(usernames, domains):
	emails = dict()
	max_confidence = max(usernames.values())
	common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com']

	username_from_email = lambda email: email[:email.index('@')]

	# Finds any emails in domain source code
	def parse_HTML(html):
		s = soup(html)
		for string in s.strings:
			match = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string)
			if match:
				emails[match.group(0)] = 1
		# If any emails are directly linked on a domain,
		# it is highly probable that it's the right email
		for email in s.select('a[href^=mailto]'):
			emails[email.string] = max_confidence

	for domain in domains:
		if domain[:4] != 'http':
			domain = 'http://' + domain
		# Might not have permission to scrape
		try:
			resp = urllib2.urlopen(domain).read()
			parse_HTML(resp)
		except:
			pass
		# Common emails of people with their own domains
		stripped_domain = strip_domain(domain)
		emails['admin@' + stripped_domain] = 0.5
		emails['info@' + stripped_domain] = 0.5
		emails['me@' + stripped_domain] = 0.5
		for username in usernames:
			emails[username + '@' + stripped_domain] = usernames[username]

	for username in usernames:
		for domain in common_domains:
			emails[username + '@' + common_domains] = usernames[username]
