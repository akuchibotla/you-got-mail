from bs4 import BeautifulSoup as soup
from checker import strip_domain
import urllib2
import string

def is_website(url):
	domain = strip_domain(url)
	url = url[url.index(domain) + len(domain):]
	if '.' not in url:
		return True

	dot = url[::-1].index('.')
	if dot == 3:
		return url[-4:] == '.html'
	return False

def crawl(url):
	domain = strip_domain(url)
	visited = set()
	fringe = [url]

	while len(fringe) > 0:
		curr = fringe.pop(0)
		if curr not in visited:
			visited.add(curr)
			s = soup(urllib2.urlopen(curr).read(), 'html.parser')
			for link in s.select('a'):
				if link.has_attr('href'):
					href = link['href'].encode('utf-8').strip()
					if href not in visited and strip_domain(href) == domain and is_website(href):
						if href[-1] == '/':
							href = href[:-1]
						fringe.append(href)
	return visited