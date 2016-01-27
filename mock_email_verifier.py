import random
import time

# Used for proof of concept so that
# the 200 API requests don't get extinguished

def verify_email(email):
	# Simulates passage of time
	time.sleep(0.1)

	# Returns 50% of emails as valid
	return random.randint(1,10) < 5