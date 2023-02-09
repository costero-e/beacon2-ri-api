import urllib.request as urllib2
from urllib.request import urlopen
from bs4 import *
from urllib.parse  import urljoin
import json


def extract_ontologies_urls(pages, depth=None):
    indexed_url = [] # a list for the main and sub-HTML websites in the main website
    for i in range(depth):
        for page in pages:
            if page not in indexed_url:
                indexed_url.append(page)
                try:
                    c = urllib2.urlopen(page)
                except:
                    print( "Could not open %s" % page)
                    continue
                soup = BeautifulSoup(c.read())
                links = soup('a') #finding all the sub_links
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                                continue
                        url = url.split('#')[0] 
                        if url[0:4] == 'http':
                                indexed_url.append(url)
        pages = indexed_url
    return indexed_url

def extract_terms(urls):
    substring = 'terms'
    term1 = '/hp/'

    new_urls = []
    for url in urls:
        if substring in url:
            if term1 in url:
                new_urls.append(url)
        else:
            continue
    return new_urls

def extract_urls_length(new_urls):
    list_of_pages=[]
    for page in new_urls:
        c = urllib2.urlopen(page)
        soup = BeautifulSoup(c.read())
        span_unit = soup.find("span", id="end-display")
        if span_unit:
            span_unit_text = span_unit.text
        span_total = soup.find("span", id="total-display")
        if span_total:
            span_total_text = span_total.text
        if span_unit and span_total:
            total_pages = int(int(span_total_text)/int(span_unit_text))
            for i in range(total_pages):
                page_complete = page + '?page=' + str(i)
                list_of_pages.append(page_complete)
                print(page_complete)
    return list_of_pages

def download_html(list_of_pages):
    list = []
    print(list_of_pages)
    for item in list_of_pages:
        print(item)
        try:
            c = urllib2.urlopen(item)
        except:
            print( "Could not open %s" % item)
            continue
        soup = BeautifulSoup(c.read())
        tds = soup('td')
        n = 0
        dict={}
        for td in tds:
            if n == 0:
                dict['label'] = td.text.replace("\n", "")
                n += 1
            elif n == 1:
                td_dots = td.text.replace("_",":")
                dict['id'] = td_dots.replace("\n", "")
                list.append(dict)
                dict={}
                n += 1
            elif n == 2:
                n = 0
                    


    print(list)
    print(len(list))
    with open("ontologies/ontologies.json", "w") as f:
        json.dump(list, f)



pagelist=["https://www.ebi.ac.uk/ols/ontologies"]
urls = extract_ontologies_urls(pagelist, depth=1)
urls_terms = extract_terms(urls)
list_new = extract_urls_length(urls_terms)
#list = ['https://www.ebi.ac.uk/ols/ontologies/zp/terms?page=2913', 'https://www.ebi.ac.uk/ols/ontologies/zp/terms?page=2914']
download_html(list_new)