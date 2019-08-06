import os
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas as pd
import googlemaps
from uuid import uuid4

@require_http_methods(['GET', 'POST'])
def home_view(request):
    if request.method == 'GET':
        return render(request, 'geocoding/home.html')

    else:
        if 'csv_file' in request.FILES and request.FILES['csv_file'].name.endswith('.csv'):
            csv_file = request.FILES['csv_file']
            if not csv_file.multiple_chunks():
                try:
                    fs = FileSystemStorage()
                    uuid_file_name = str(uuid4())
                    filename = fs.save(f'{uuid_file_name}.csv', csv_file)
                    os_file_path = f'{settings.MEDIA_ROOT}/{filename}'
                    addresses = pd.read_csv(os_file_path, usecols=['address'], nrows=6)
                    print(addresses)
                    lat_lng = []
                    for address in addresses.iterrows():
                        clean_address = str(address[1]).split('Name')[0].split('address')[1].strip()
                        geocode_result = do_geocoding(clean_address)

                        if geocode_result['success']:
                            lat, lng = geocode_result['lat'], geocode_result['lng']
                            lat_lng.append(f'{lat}, {lng}')
                        else:
                            lat_lng.append('NOT FOUND')
                    if lat_lng:
                        write_to_csv(os_file_path, lat_lng)
                        file_url = fs.url(filename)
                        hostname = request.META['HTTP_HOST']
                        public_file_path = f'http://{hostname}{file_url}'
                        return HttpResponseRedirect(public_file_path)
                    else:
                        return HttpResponse('Cannot Geocode any address!')

                except Exception as e:
                    error_message = f'Error! {str(e)}'
                    return HttpResponse(error_message)

            else:
                return HttpResponse('File is too large!')

        else:
            return HttpResponse('Error! Please upload proper CSV files only!')


def do_geocoding(address):
    GOOGLE_MAPS_GEOCODING_API_KEY = os.environ.get('GOOGLE_MAPS_GEOCODING_API_KEY')
    if GOOGLE_MAPS_GEOCODING_API_KEY is not None:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_GEOCODING_API_KEY)
        api_response = gmaps.geocode(address)

        if api_response:
            geocode_result = {'success': True, 'lat': api_response[0]['geometry']['location']['lat'], \
                'lng': api_response[0]['geometry']['location']['lng']}
        else:
            geocode_result = {'success': False, 'message': 'Address not found by Google!'}

        return geocode_result
    else:
        raise Exception('Error in Google API key configuration!')


def write_to_csv(csv_url, lat_lng):
    f = pd.read_csv(csv_url, nrows=6)
    f['lat_lng'] = lat_lng
    f.to_csv(csv_url)
    return csv_url