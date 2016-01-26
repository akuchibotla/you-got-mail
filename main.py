from email_verifier import verify_email
from generator import username_generator, email_generator

def main(first_name, last_name, middle_name=None, linkedin_url=None, twitter_url=None, angellist_url=None, github_url=None, domains=[]):
	usernames = username_generator(first_name, last_name, middle_name, domains, linkedin_url, angellist_url, twitter_url, github_url)
	emails = email_generator(usernames, domains, [linkedin_url, twitter_url, angellist_url, github_url])
	email_confidence = [(addr, emails[addr]) for addr in emails]
	email_confidence.sort(key=lambda x: -x[1])
	for addr, conf in email_confidence:
		if verify_email(addr):
			print addr, 'is the correct email with confidence', conf