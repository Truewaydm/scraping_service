import asyncio
import codecs
import os, sys

from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from django.db import DatabaseError

from parser import *
from scraping.models import Vacancy, City, Language, Errors, Url

User = get_user_model()

parser = (
    (work_ua, 'work_ua'),
    (dou_ua, 'dou_ua'),
    (djinni_co, 'djinni_co'),
    (rabota_ua, 'rabota_ua')
)

jobs, errors = [], []


def get_settings():
    query_set = User.objects.filter(send_email=True).values()
    settings_list = set((qs['city_id'], qs['language_id']) for qs in query_set)
    return settings_list


def get_urls(settings):
    query_set = Url.objects.all().values()
    url_dict = {(qs['city_id'], qs['language_id']): qs['url_data'] for qs in query_set}
    urls = []
    for pair in settings:
        if pair in url_dict:
            temp = {}
            temp['city'] = pair[0]
            temp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                temp['url_data'] = url_dict.get(pair)
                urls.append(temp)
    return urls


async def main(value):
    func, url, city, language = value
    job, error = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(error)
    jobs.extend(job)


setting = get_settings()
url_list = get_urls(setting)

# city = City.objects.filter(slug='kyiv').first()
# language = Language.objects.filter(slug='python').first()

loop = asyncio.get_event_loop()
temp_task = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parser]
tasks = asyncio.wait([loop.create_task(main(func)) for func in temp_task])
# for data in url_list:
#     for func, key in parser:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e
loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    variable = Vacancy(**job)
    try:
        variable.save()
    except DatabaseError:
        pass
    if errors:
        error = Errors(data=f'errors:{errors}').save()

# work_result = codecs.open('parser_vacancy.json', 'w', 'utf-8')
# work_result.write(str(jobs))
# work_result.close()
