import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soap = BeautifulSoup(data, features='html.parser')
    post_listings = soap.find_all('li', {'class': 'result-row'})
    #post_titles = post_listings[0].find(class_='result-title').text
    #post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find(class_='result-price').text
    #print(post_titles)
    #print(post_url)
    #print(post_price)

    # print(post_titles[0].text)
    # print(search)
    # print(data)
    # print(quote_plus(search))
    # print(final_url)

    final_posting = []
    for post in post_listings:

        post_titles = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price= ('N/A')

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting.append((post_titles,post_url,post_price,post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
