import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


def work_ua(url):
    jobs: list = []
    errors: list = []
    domain: str = 'https://www.work.ua'
    url: str = 'https://www.work.ua/jobs-kyiv-python/'
    work_request = requests.get(url, headers=headers)
    if work_request.status_code == 200:
        soup = BS(work_request.content, 'html.parser')
        main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                description = div.a.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': domain + href, 'description': description, 'company': company})
        else:
            errors.append({'url': url, 'title': 'div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def rabota_ua(url):
    jobs: list = []
    errors: list = []
    domain: str = 'https://rabota.ua/ua'
    work_request = requests.get(url, headers=headers)
    if work_request.status_code == 200:
        soup = BS(work_request.content, 'html.parser')
        main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                description = div.a.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': domain + href, 'description': description, 'company': company})
        else:
            errors.append({'url': url, 'title': 'div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    jobs, errors = rabota_ua(url)
    work_result = codecs.open('work.text', 'w', 'utf-8')
    work_result.write(str(jobs))
    work_result.close()
