from datetime import datetime
import requests
import json
import os

from app.settings import EBAY_APP_ID


def formatTime(time_date):
    formatted_dt = datetime.strptime(time_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return formatted_dt.strftime('%I:%M %p')


def formatDate(time_date):
    formatted_dt = datetime.strptime(time_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return formatted_dt.strftime('%Y-%m-%d')


"""
def api_query(query):
    if query:
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': EBAY_APP_ID,
            'SERVICE-VERSION': '1.0.0',
            'keywords': query,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'paginationInput.entriesPerPage': '20'
        }
        api_url = 'https://svcs.ebay.com/services/search/FindingService/v1'
        response = requests.get(url=api_url, params=metadata)
        if response.status_code == 200:
            json_data = response.json()
            if json_data['findItemsByKeywordsResponse'][0]['errorMessage']:
                return None
            return json_data
        else:
            print("Request Failed!")
            return None
    print('Query String was empty')
    return None
"""


def api_query(query=None, numberOfProducts=0, minPrice=0, maxPrice=0):
    metadata = {}
    if query is not None and query != '' \
            and numberOfProducts > 0 and minPrice > 0 and maxPrice > 0:
        print("CALLED 1")
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': os.environ.get('PROD_APP_ID'),
            'SERVICE-VERSION': '1.0.0',
            'keywords': query,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'paginationInput.entriesPerPage': numberOfProducts,
            'itemFilter.name': 'MinPrice',
            'itemFilter.value': minPrice,
            'itemFilter.name': 'MaxPrice',
            'itemFilter.value': maxPrice,
            'itemFilter.paramName': 'Currency',
            'itemFilter.paramValue': 'USD',
        }
    elif query is not None and query != '' and minPrice > 0 and maxPrice > 0:
        print("CALLED 5")
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': os.environ.get('PROD_APP_ID'),
            'SERVICE-VERSION': '1.0.0',
            'keywords': query,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'itemFilter.name': 'MinPrice',
            'itemFilter.value': minPrice,
            'itemFilter.name': 'MaxPrice',
            'itemFilter.value': maxPrice,
            'itemFilter.paramName': 'Currency',
            'itemFilter.paramValue': 'USD'
        }
    elif query is not None and query != '' and numberOfProducts > 0:
        print("CALLED 2")
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': os.environ.get('PROD_APP_ID'),
            'SERVICE-VERSION': '1.0.0',
            'keywords': query,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'paginationInput.entriesPerPage': numberOfProducts,
        }
    elif query is not None and query != '' and minPrice > 0:
        print("CALLED 3")
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': os.environ.get('PROD_APP_ID'),
            'SERVICE-VERSION': '1.0.0',
            'keywords': query,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'itemFilter.name': 'MinPrice',
            'itemFilter.value': minPrice,
            'itemFilter.paramName': 'Currency',
            'itemFilter.paramValue': 'USD'
        }
    elif query is not None and query != '' and maxPrice > 0:
        print("CALLED 4")
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': os.environ.get('PROD_APP_ID'),
            'SERVICE-VERSION': '1.0.0',
            'keywords': query,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'itemFilter.name': 'MaxPrice',
            'itemFilter.value': maxPrice,
            'itemFilter.paramName': 'Currency',
            'itemFilter.paramValue': 'USD'
        }
    elif query is not None and query != '':
        print("6")
        metadata = {
            'OPERATION-NAME': 'findItemsByKeywords',
            'SECURITY-APPNAME': os.environ.get('PROD_APP_ID'),
            'SERVICE-VERSION': '1.0.0',
            'RESPONSE-DATA-FORMAT': 'JSON',
            'keywords': query,
        }
    api_url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    if metadata is not None:
        response = requests.get(url=api_url, params=metadata)
        print(response)
        if response.status_code == 200:
            json_data = response.json()
            try:
                if json_data['findItemsByKeywordsResponse'][0]['errorMessage']:
                    return None
            except:
                pass
            return json_data
        else:
            print("Request Failed!")
            return None
        print('Query String was empty')
    return None


def get_data(json_response):
    if json_response:
        products = []
        data = \
            json_response['findItemsByKeywordsResponse'][0]['searchResult'][0]['@count']
        data_count = int(data)
        items = \
            json_response['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']
        try:
            for i in range(data_count):
                product = {}
                product["item_condition"] = items[i]['condition'][0]['conditionDisplayName'][0]
                product["image_url"] = items[i]['galleryURL'][0]
                product["item_id"] = items[i]['itemId'][0]
                product["best_available_offer"] = items[i]['listingInfo'][0]['bestOfferEnabled'][0]
                product["buy_now_available"] = items[i]['listingInfo'][0]['buyItNowAvailable'][0]
                start_datetime = items[i]['listingInfo'][0]['startTime'][0]
                product["start_date"] = formatDate(start_datetime)
                product["start_time"] = formatTime(start_datetime)
                end_datetime = items[i]['listingInfo'][0]['endTime'][0]
                product["end_date"] = formatDate(end_datetime)
                product["end_time"] = formatTime(end_datetime)
                product["category_id"] = items[i]['primaryCategory'][0]['categoryId'][0]
                product["category_name"] = items[i]['primaryCategory'][0]['categoryName'][0]
                product["returns_accepted"] = items[i]['returnsAccepted'][0]
                product["current_price_currency"] = \
                    items[i]['sellingStatus'][0]['convertedCurrentPrice'][0]['@currencyId']
                product["current_price"] = \
                    items[i]['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__']
                product['selling_status'] = items[i]['sellingStatus'][0]['sellingState'][0]
                product['title'] = items[i]['title'][0]
                if items[i].get('subtitle') is not None:
                    product['subtitle'] = items[i]['subtitle'][0]
                product['item_url'] = items[i]['viewItemURL'][0]
                products.append(product)
            return products
        except:
            pass
    else:
        return None
    return None


# Main
"""
raw_data = api_query('iphone')
products = get_data(raw_data)
for index in range(len(products)):
    print(products[index]['title'])
"""
