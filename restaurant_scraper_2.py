import json as js
import bs4  
from lxml import html
import json as js
from urllib.request import Request, urlopen
import math


# from selenium import webdriver
# driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

url_model = "{}/business-directory/company-information.fast-food-quick-service-restaurants.nl.{}.{}.html?page={}"
parent_page = "https://www.dnb.com"
numberOfPageLoaded = 0

# resp=requests.get(final_url)
def getChildLinksFromParentLink(num, province, city, home = parent_page,model = url_model):

    final_url = model.format(home , province , city, num)

    req = Request(final_url.encode('ascii', 'ignore').decode('ascii'), headers={'User-Agent': 'XYZ/3.0'})
    webpage= urlopen(req).read()

    # soup=bs4.BeautifulSoup(webpage,'lxml')
    tree = html.fromstring(webpage)
    xPath_to_restaurant_list = '//div[@class="col-md-12 data"]/div[@class="col-md-6"]/a//@href'
    linksToRestaurantPage = tree.xpath(xPath_to_restaurant_list)
    return [home + eachLink for eachLink in linksToRestaurantPage]


def testNone(var):
    if var == None:
        return "None"
    return var.text.strip()
def returnValueOnPage(exLink):

    sub_req = Request(exLink.encode('ascii', 'ignore').decode('ascii'), headers={'User-Agent': 'XYZ/3.0'})
    sub_webpage= urlopen(sub_req).read()
    soup=bs4.BeautifulSoup(sub_webpage,'lxml')

    title = soup.find('h1', class_="title")
    title = testNone(title)

    tradeName = soup.find('div', class_ = "tradeName")
    tradeName = testNone(tradeName)

    street_address_1 = soup.find('div', class_ = "street_address_1")
    street_address_1= testNone(street_address_1)

    company_postal = soup.find('span', class_ = 'company_postal')
    company_postal = testNone(company_postal)

    company_region = soup.find('span', class_ = 'company_region')
    company_region = testNone(company_region)

    type_company = soup.find('span', class_ = "type")
    type_company = testNone(type_company)

    role_company = soup.find('span', class_ = "role")
    role_company = testNone(role_company)

    phone = soup.find('div', class_ = 'phone')
    phone = testNone(phone)
        
    
    value_list = soup.findAll('span', class_ = "value")
    value_text_list = []
    for value in value_list[:3]:
        value = testNone(value)
        value_text_list.append(value)
    rev_title = soup.find('div', class_ = "rev_title")
    if rev_title !=None:
        rev_title = rev_title.text[-4:]
    else:
        rev_title = "None"


    return (title , tradeName , street_address_1 , 
            company_postal , company_region , type_company , 
            role_company , phone , rev_title, 
            value_text_list[1] , value_text_list[0] , value_text_list[2])
def writeToCSV(listChildLink):
    fp = open("dataFastfood.csv","a+")

    for eachLink in listChildLink:
        global numberOfPageLoaded
        numberOfPageLoaded +=1

        try:
            valueReturned = returnValueOnPage(eachLink)
            for i,eachValue in enumerate(valueReturned):

                fp.write(eachValue)
                fp.write(" ; ")
            fp.write("\n")
            print("Number of page loaded:",numberOfPageLoaded)
            print("Success:",eachLink)
            print()
            trackingFile = open("trackingFile_5","a",encoding="utf-8")
            trackingFile.write("Number of page loaded:"+str(numberOfPageLoaded)+"\n")
            trackingFile.write("Success: "+eachLink.encode('utf-8','ignore').decode("utf-8")+"\n\n")
            trackingFile.close()
        except:
            print("Number of page loaded:",numberOfPageLoaded)
            print("Fail:",eachLink)
            print()
            trackingFile = open("trackingFile_5","a")
            trackingFile.write("Number of page loaded:"+str(numberOfPageLoaded)+"\n")
            trackingFile.write("Fail: "+eachLink.encode('utf-8','ignore').decode("utf-8")+"\n\n")
            trackingFile.close()
            continue
    fp.close()
def main():    
    fp_json = open("dataFastfood.json")
    provinceJSON = js.load(fp_json)
    for eachProvince in provinceJSON:
        provinceName = eachProvince["provinceName"]
        childCityList = eachProvince['childCityList']

        for eachChildCity in childCityList:
            cityName = eachChildCity["cityName"]
            numRestaurant = int(eachChildCity["numChildPage"])
            numPages = list(range(1,math.ceil(numRestaurant/50)+1))
            for eachNum in numPages:
                listChildPage = getChildLinksFromParentLink(eachNum, provinceName, cityName)
                writeToCSV(listChildPage)

    fp_json.close()

if __name__ == "__main__":
    main()
# def return_tuple_contain_None():
#     return("1,3","34","None")
# fp.write("None")
# fp.write("13")
# fp.write("No334ne")
# print(";".join(return_tuple_contain_None()))