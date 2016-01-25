from mock_email_verifier import verify_email
from generator import username_generator, email_generator

def main(first_name, last_name, middle_name=None, linkedin_url=None, twitter_url=None, angellist_url=None, github_url=None, domains=[]):
	usernames = username_generator(first_name, last_name, middle_name, domains, linkedin_url, angellist_url, twitter_url, github_url)
	emails = email_generator(usernames=usernames, domains=domains, links=[linkedin_url, twitter_url, angellist_url, github_url])
	email_confidence = [(addr, emails[addr]) for addr in emails]
	email_confidence.sort(key=lambda x: -x[1])
	num = 5
	for addr, conf in email_confidence:
		answer, num = verify_email(addr, num)
		if answer:
			print addr, 'is the correct email with confidence', conf

main(first_name='Anand', last_name='Kuchibotla', linkedin_url='http://linkedin.com/in/akuchibotla', github_url='github.com/akuchibotla', domains=['akuchibotla.com'])