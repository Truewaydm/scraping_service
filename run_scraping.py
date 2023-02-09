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
    (work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (djinni_co, 'https://djinni.co/jobs/?primary_keyword=Python'),
    (rabota_ua, 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2')
)


def get_settings():
    query_set = User.objects.filter(send_email=True).values()
    settings_list = set((qs['city_id'], qs['language_id']) for qs in query_set)
    return settings_list


def get_urls(_settings):
    query_set = Url.objects.all().values()
    url_dict = {(qs['city_id'], qs['language_id']): qs['url_data'] for qs in query_set}
    urls = []
    for pair in _settings:
        temp = {}
        temp['city'] = pair[0]
        temp['language'] = pair[1]
        temp['url_data'] = url_dict[pair]
        urls.append(temp)
    return urls


get_user_city_id_and_language_id = get_settings()
get_url = get_urls(get_user_city_id_and_language_id)

city = City.objects.filter(slug='kyiv').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    variable = Vacancy(**job, city=city, language=language)
    try:
        variable.save()
    except DatabaseError:
        pass
    if errors:
        error = Errors(data=errors).save()

# work_result = codecs.open('parser_vacancy.json', 'w', 'utf-8')
# work_result.write(str(jobs))
# work_result.close()
