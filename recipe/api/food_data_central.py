import requests

from django.conf import settings
from django.http import JsonResponse

api_base_url = 'https://api.nal.usda.gov/fdc/v1/'
api_key = settings.FDC_API_KEY


def search_food(ingredient):
    params = {
        'api_key': api_key,
        'query': ingredient,
        'pageSize': 1,
    }
    endpoint = 'foods/search/'
    response = requests.get(api_base_url + endpoint, params=params)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}

# def get_fdc_data():
#     params = {
#     'api_key': api_key,
#     'pageSize': 2
#     }
#     endpoint = 'food/2353623'
#     response = requests.get(api_base_url+endpoint, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'error': 'Failed to fetch data'}, status=500)