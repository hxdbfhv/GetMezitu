import requests
from bs4 import BeautifulSoup

def get_image_url(url):
	html_content = requests.get(url).text
	soup = BeautifulSoup(html_content,"lxml") #lxml???
	html_image_url = soup.select("#pins li span a")
	urls = []
	for url in html_image_url:
		url = url.get('href')  # href???
		urls.append(url)
	return urls

def get_image(url):
	try:
		q = requests.get(urls=url,headers=head).text
		image = re.search(r'<img src="(.*)" alt=',q)
		return image
	except:
		pass
		

if __name__=="__main__":
	head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer': 'http://www.mzitu.com/37288/3'}
    url = "http://www.mzitu.com/xinggan"
    url_list = get_image_url(url)

    for i in url_list:
    	image_url = get_image(i)
    	image = requests.get(urls=image_url,headers=head)
    	with open("%d.jpg"%i,"wb") as f:
    		f.write(image.content)

