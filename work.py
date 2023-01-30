import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }
domain: str = 'https://www.work.ua'
url: str = 'https://www.work.ua/jobs-kyiv-python/'
work_request = requests.get(url, headers=headers)
jobs: list = []
if work_request.status_code == 200:
    soup = BS(work_request.content, 'html.parser')
    main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
    div_list = main_div.find_all('div', attrs={'class': 'job-link'})
    for div in div_list:
        title = div.find('h2')
        href = title.a['href']
        description = div.a.text
        company = 'No name'
        logo = div.find('img')
        if logo:
            company = logo['alt']

work_header = codecs.open('work.html', 'w', 'utf-8')
work_header.write(str(work_request.text))
work_header.close()
