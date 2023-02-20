import os, sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()
from scraping.models import Vacancy, Errors
from scraping_service.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject = f'Newsletter of vacancies for {today}'
text_content = f'Newsletter of vacancies {today}'
from_email = EMAIL_HOST_USER
empty = '<h2>Unfortunately, there is no data for your preferences at the moment.</h2>'
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
        # [:10] - 10 vacancies, if empty, view all vacancies
    query_set_vacancy = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in query_set_vacancy:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3"><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

query_set_errors = Errors.filter(timestamp=today)
if query_set_errors.exists():
    error = query_set_errors.first()
    data = error.data
    _html = ''
    for i in data:
        _html += f'<p"><a href="{i["url"]}">Error: {i["title"]}</a></p>'
        subject = ''
        text_content = ''
        to = ADMIN_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()

# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()
