import requests

from django.conf import settings
from django.http import JsonResponse

# api_url = 'https://api.nal.usda.gov/fdc/v1/'
# api_key = settings.FDC_API_KEY



def get_fdc_data():
    pass
#     params = {
#     'api_key': api_key,
#     'pageSize': 2
#     }
#     endpoint = 'foods/list/'
#     response = requests.get(api_url+endpoint, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'error': 'Failed to fetch data'}, status=500)