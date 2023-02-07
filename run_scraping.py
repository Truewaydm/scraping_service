import codecs
import os, sys

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from parser import *
from scraping.models import Vacancy, City, Language

parser = (
    (work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (djinni_co, 'https://djinni.co/jobs/?primary_keyword=Python'),
    (rabota_ua, 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2')
)

city = City.objects.filter(slug='kyiv')

jobs, errors = [], []
for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e

work_result = codecs.open('parser_vacancy.json', 'w', 'utf-8')
work_result.write(str(jobs))
work_result.close()
