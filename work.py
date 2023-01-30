import requests
import codecs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }

url = 'https://www.work.ua/jobs-kyiv-python/'
work_request = requests.get(url, headers=headers)
work_header = codecs.open('work.html', 'w', 'utf-8')
work_header.write(str(work_request.text))
work_header.close()
