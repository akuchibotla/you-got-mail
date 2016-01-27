import string

url_chars = set([char for char in string.ascii_lowercase] + ['.'])

# Utility function that is called throughout program
def strip_domain(domain):
	if len(domain) > 3:
		start = 7
		if domain[4] == 's':
			if domain[8:11] == 'www':
				start = 12
			else:
				start = 8
		elif domain[7:10] == 'www':
			start = 11
		end = start
		while end < len(domain) and domain[end] in url_chars:
			end += 1
		return domain[start:end]