import random

# Used for proof of concept so that
# the 200 API requests don't get extinguished

def verify_email(email, emails_to_return):
	answer = False
	if emails_to_return > 0:
		result = random.randint(1,10)
		if result < emails_to_return:
			emails_to_return -= 1
			answer = True
	return answer, emails_to_return