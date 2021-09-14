from celery import shared_task
import httplib2
from bs4 import BeautifulSoup,SoupStrainer

def get_page():
    http = httplib2.Http()
    status, page = http.request('https://www.allsafe.in/')
    return page

@shared_task
def get_website_title():
    response=get_page()
    soup=BeautifulSoup(response,"html.parser")
    return {"Title":[soup.find("title").get_text()]}
    

@shared_task
def get_services_of_allsafe():
    all_services=[]
    response=get_page()
    soup=BeautifulSoup(response,"html.parser")
    for service in soup.find_all("p",'font-weight-bold'):
        all_services.append(service.get_text())
    
    return {"Services":all_services}

@shared_task
def get_all_links():
    all_links=[]
    response=get_page()
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href') and len(link['href'])>4:
            if link['href'][:4]!="http":
                link['href']="https://www.allsafe.in"+str(link['href'])
            all_links.append(link['href'])
    
    return {"Links":all_links}
