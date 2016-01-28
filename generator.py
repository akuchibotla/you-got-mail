from bs4 import BeautifulSoup as soup
from crawler import crawl
from utils import strip_domain
import string
import urllib2
import re

# Finds any emails in domain source code
def parse_HTML(html):
	emails = list()
	s = soup(html, 'html.parser')
	for s_elem in s.strings:
		for word in s_elem.split():
			match = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", word)
			if match:
				emails.append(match.group(0).encode('utf-8').strip())

	# Return emails
	return [email.string.encode('utf-8').strip() for email in s.select('a[href^=mailto]')] + emails

# Generates usernames with a higher weightage for more probable usernames
def username_generator(first_name, last_name, middle_name=None, domains=[], linkedin_url=None, angellist_url=None, twitter_url=None, facbeook_url=None, github_url=None):
	usernames = dict()
	username_chars = set([char for char in string.ascii_lowercase] + [str(i) for i in range(10)] + ['_', '-', '.'])

	# Adds usernames to the username set
	def add_username(username, link=False):
		username = username.lower().replace('-', '_')
		if link:
			if username in usernames:
				usernames[username] += 3
			else:
				usernames[username] = 3
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

			username = url[start:end]
			add_username(username, link=True)

	for url in [(linkedin_url, 'linkedin.com/in/'), (angellist_url, 'angel.co/'), (twitter_url, 'twitter.com/'), (github_url, 'github.com/'), (facbeook_url, 'facebook.com/')]:
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
		if domain[:4] != 'http':
			domain = 'http://' + domain
		stripped_domain = strip_domain(domain)
		add_username(stripped_domain[:stripped_domain.index('.')])

	# Weights usernames on their content
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
		usernames[username] *= username_weight(username)

	return usernames
		
# Generates potential email addresses
def email_generator(usernames, domains=[], links=[]):
	emails = dict()
	max_confidence = max(usernames.values())
	common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com']

	username_from_email = lambda email: email[:email.index('@')]

	for domain in domains:
		if domain[:4] != 'http':
			domain = 'http://' + domain
		# Might not have permission to scrape
		try:
			internal_links = crawl(domain)
			for l in internal_links:
				resp = urllib2.urlopen(l).read()
				parsed_emails = parse_HTML(resp)
				for email in parsed_emails:
					emails[email] = max_confidence
		except:
			pass

		# Common emails of people with their own domains
		# If any of these exist, the chance of it being their email
		# is highly likely since it's a personal domain
		stripped_domain = strip_domain(domain)
		emails['admin@' + stripped_domain] = max_confidence
		emails['info@' + stripped_domain] = max_confidence
		emails['me@' + stripped_domain] = max_confidence

	for link in links:
		if link:
			if link[:4] != 'http':
				link = 'http://' + link
			# Might not have permission to scrape
			try:
				resp = urllib2.urlopen(link).read()
				parsed_emails = parse_HTML(resp)
				for email in set(parsed_emails):
					if email in emails:
						emails[email] *= 1.5
					else:
						emails[email] = max_confidence
			except:
				pass

	for username in usernames:
		for domain in common_domains:
			email = username + '@' + domain
			if email in emails:
				emails[username + '@' + domain] += usernames[username]
			else:	
				emails[username + '@' + domain] = usernames[username]

	return emails
