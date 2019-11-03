from django.shortcuts import render
import requests
from lxml import html
from requests.compat import quote_plus


# Create your views here.
def home (request):
    return render(request, 'base.html')
def new_search(request):
    search = request.POST.get('search')
    print(search)
    session = requests.Session()
    r = session.get("https://www.craigslist.org/")
    city = session.cookies.get_dict()['cl_def_hp']
    base_url = 'https://{}.craigslist.org/search/bbb?query='.format(city)
    final_url = base_url+quote_plus(search)
    response = requests.get(final_url)
    element_tree = html.fromstring(response.text)
    information_list = element_tree.xpath("//li[@class='result-row']")
    final_posting = []
    for inf in  information_list:
        anchor_tag = inf.xpath('.//p/a')
        title = anchor_tag[0].text
        url = anchor_tag[0].get('href')
        price = inf.xpath(".//a/span[@class='result-price']")
        if len(price)==0:
            price = 'N/A'
        else:
            price = price[0].text
        '''Logic to find image'''
        a=inf.xpath('.//a')
        image_inf = a[0].get('data-ids')
        if image_inf:
            image_id = image_inf.split(':')[-1]
            image_url = "https://images.craigslist.org/{}_300x300.jpg".format(image_id)
        else:
            image_url = "https://www.carechartsuk.co.uk/wp-content/uploads/2015/09/NO-IMAGE-AVAILABLE-ICON-web1.jpg"
        print(image_url)
        final_posting.append((title, url, price, image_url))
    # print(final_posting)
    search_stuff = {
        'search': search,
        'final_postings': final_posting,
    }
    return  render( request, 'myapp/new_search.html', search_stuff)