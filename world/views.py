from django.db.models import F
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required


from world.models import Country, City, Countrylanguage
from world.serializer import SearchResultSerializer


@api_view(['GET', ])
def search_select2(request):
    search_text = request.GET.get('search_text', False)
    if search_text:
        countries = Country.objects.filter(name__icontains=search_text) \
            .annotate(id=F('code'), text=F('name')).values('id', 'text').distinct()
        cities = City.objects.filter(name__icontains=search_text) \
            .annotate(text=F('name')).values('id', 'text').distinct()
        languages = Countrylanguage.objects.filter(language__icontains=search_text) \
            .annotate(id=F('language'), text=F('language')).values('id', 'text').distinct()
        countries = list(map(lambda c: c.update({'type': 'country'}) or c, countries))
        cities = list(map(lambda c: c.update({'type': 'city'}) or c, cities))
        languages = list(map(lambda c: c.update({'type': 'language'}) or c, languages))
        results = countries + cities + languages
        serializer = SearchResultSerializer(results, many=True)
        return Response(data=serializer.data)
    return Response(data=[])

@login_required
def get_country(request, code):
    try:
        country = Country.objects.get(code=code)
    except Country.DoesNotExist:
        country = None
    return render(request, 'world/country.html', {'country': country})

@login_required
def get_city(request, id):
    city = get_object_or_404(City, id=id)
    return render(request, 'world/city.html', {'city': city})

@login_required
def get_country_language(request, language):
    languages = Countrylanguage.objects.filter(language=language)
    return render(request, 'world/language.html', {'languages': languages,'language': language })

@login_required
def search(request, search_type):
    search = request.GET.get('search', False)
    if search:
        if search_type == "country":
            response = get_country(request, code=search)
        elif search_type == "city":
            response = get_city(request, id=search)
        elif search_type == "language":
            response = get_country_language(request, language=search)
        return response
    else:
        raise Http404
