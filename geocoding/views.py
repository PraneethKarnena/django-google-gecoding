from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET', 'POST'])
def home_view(request):
    if request.method == 'GET':
        return render(request, 'geocoding/home.html')

    else:
        pass