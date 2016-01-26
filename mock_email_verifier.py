import random

# Used for proof of concept so that
# the 200 API requests don't get extinguished

def verify_email(email):
	return random.randint(1,10) < 3