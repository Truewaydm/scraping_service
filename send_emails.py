import os, sys

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()
from scraping.models import Vacancy

User = get_user_model()
query_set_users = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in query_set_users:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    # __in - find all params in DB city_id, language_id
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    query_set_vacancy = Vacancy.objects.filter(**params)[:10]

subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
text_content = 'This is an important message.'
html_content = '<p>This is an <strong>important</strong> message.</p>'
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")
msg.send()
