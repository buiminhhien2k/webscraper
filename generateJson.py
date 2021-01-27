import bs4  
from lxml import html
import json as js
from urllib.request import Request, urlopen

json_output = []
home ="https://www.dnb.com"
url ="/business-directory/company-information.fast-food-quick-service-restaurants.nl.html"
final_url = home +url

req = Request(final_url, headers={'User-Agent': 'XYZ/3.0'})
webpage= urlopen(req).read()

# soup=bs4.BeautifulSoup(webpage,'lxml')
soup=bs4.BeautifulSoup(webpage,'lxml')

provinceList= soup.findAll('div', class_ = "col-md-6 col-xs-6 data")
i = 0
for eachProvince in provinceList:
    linkToProvince = home + eachProvince.find('a')['href']
    provinceName = eachProvince.find('a').text.strip().split(" ")[0]
    numChildPage = eachProvince.find('span').text.strip()[1:-1]
    if "," in numChildPage:
        numChildPage = numChildPage.replace(",","")
    json_output.append({
        "provinceName":provinceName,
        "numChildPage":numChildPage
    })

    childCityList = []
    sub_req = Request(linkToProvince, headers={'User-Agent': 'XYZ/3.0'})
    sub_webpage= urlopen(sub_req).read()

    # soup=bs4.BeautifulSoup(webpage,'lxml')
    sub_soup=bs4.BeautifulSoup(sub_webpage,'lxml')
    cityList = sub_soup.findAll("div", class_ = "col-md-6 col-xs-6 data")
    for eachCity in cityList:
        cityName = eachCity.find('a').text.strip().split(" ")[0].encode('utf-8','ignore').decode("utf-8").replace("\u00a0","_")
        if "'t" in cityName:
            cityName = cityName.replace("-","_").replace("\u00a0","_")
        elif "'s" in cityName:
            cityName = cityName.replace("_",'-')
        numChildPage = eachCity.find('span').text.strip()[1:-1]
        if "," in numChildPage:
            numChildPage = numChildPage.replace(",","")
        childCityList.append({
            "cityName":cityName,
            "numChildPage":numChildPage
        })
    json_output[i]["childCityList"] = childCityList
    i+=1

fp = open("dataFastfood.json",'w')
js.dump(json_output,fp)
fp.close()