from functions import searchIn, toDict, descriptionContains, readPageToHtml, writeToJson


if __name__ == '__main__':
    URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    htmlData = readPageToHtml(URL)

    outputList = []
    infoBodyList = searchIn(htmlData, 'div', {'class':'vacancy-serp-item-body__main-info'}, findAll=True)
    link = searchIn(str(infoBodyList[0]), 'a', {'data-qa':'serp-item__title'})['href']
    for vacancyInfo in infoBodyList:
        infoDict = toDict(vacancyInfo)
        if descriptionContains(infoDict['link'], r"[Dd]jango.*[Ff]lask"):
            outputList.append(infoDict)

    writeToJson(outputList)