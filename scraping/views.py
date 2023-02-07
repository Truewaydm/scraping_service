from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


# Create your views here.

def home_view(request):
    # print(request.GET)
    form = FindForm()

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        list_filter = {}
        if city:
            list_filter['city__slug'] = city
        if language:
            list_filter['language__slug'] = language

        query_set = Vacancy.objects.filter(**list_filter).select_related('city', 'language')
        paginator = Paginator(query_set, 10)  # Show 10 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
