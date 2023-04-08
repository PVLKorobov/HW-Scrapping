from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import re
import json


def readPageToHtml(url):
    fakeHeaders = Headers(browser='chrome', os='win')
    return requests.get(url, headers=fakeHeaders.generate()).text

def searchIn(html, searchTag, searchFeatures:dict, findAll = False):
    soup = BeautifulSoup(html, 'lxml')
    if findAll:
        return soup.findAll(searchTag, searchFeatures)
    else:
        return soup.find(searchTag, searchFeatures)
    
def descriptionContains(url, regex) -> bool:
    descPageHtml = readPageToHtml(url)
    desc = searchIn(descPageHtml, 'div', {'data-qa':'vacancy-description'})
    return re.search(regex, str(desc)) != None
    
def toDict(vacancyInfo) -> dict:
    title = searchIn(str(vacancyInfo), 'a', {'data-qa':'serp-item__title'}).text
    link = searchIn(str(vacancyInfo), 'a', {'data-qa':'serp-item__title'})['href']
    try:
        salary = searchIn(str(vacancyInfo), 'span', {'data-qa':'vacancy-serp__vacancy-compensation'}).text
    except:
        salary = 'з/п не указана'
    employer = searchIn(str(vacancyInfo), 'a', {'data-qa':'vacancy-serp__vacancy-employer'}).text
    city = searchIn(str(vacancyInfo), 'div', {'data-qa':'vacancy-serp__vacancy-address'}).text

    return {'title':str(title), 'link':str(link), 'salary':str(salary), 'employer':str(employer), 'city':str(city)}

def writeToJson(data:list|dict):
    with open('vacancies.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)