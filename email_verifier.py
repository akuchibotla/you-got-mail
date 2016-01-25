import urllib2
import json

# Issuing API call to Email Hippo
# Free API key limited to 200 hits
def verify_email(email, key='C1C29733'):
	url = "https://api1.27hub.com/api/emh/a/v2"
	resp = urllib2.urlopen(url + '?e=' + email + '&k=' + key)
	data = json.load(resp)
	return data['result'] == 'Ok'