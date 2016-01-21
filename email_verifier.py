import urllib2

def verify_email(email, key='C1C29733'):
	url = "https://api1.27hub.com/api/emh/a/v2"
	resp_str = urllib2.urlopen(url + '?e=' + email + '&k=' + key).read().replace('false', 'False').replace('true', 'True')
	exec 'resp_dict = ' + resp_str
	if resp_dict['result'] == 'Ok':
		return True
	else:
		return False