import requests
import codecs
import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver

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
                description = div.p.text
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
    # url: str = 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    rabota_ua_request = requests.get(url, headers=headers)
    if rabota_ua_request.status_code == 200:
        soup = BS(driver.page_source, 'html.parser')
        main_div = soup.find('div', attrs={'class': 'santa-flex santa-flex-col santa-gap-y-20'})
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'santa--mb-20 ng-star-inserted santa-min-h-0'})
            for div in div_list:
                title = div.find('h2')
                href = div.a['href']
                description = div.span.text
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
    work_result = codecs.open('parser_vacancy.json', 'w', 'utf-8')
    work_result.write(str(jobs))
    work_result.close()
