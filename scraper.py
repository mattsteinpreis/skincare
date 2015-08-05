from bs4 import BeautifulSoup
import re
import urllib2
import json

PRICE_RE = re.compile('^\$([0-9]+\.[0-9]{2})')
PRICEOLD_RE = re.compile('\$([0-9]+\.[0-9]{2})')
nPerPage = 72
nPages = 83 #need to generalize this

def getsoup(url):
    for attempt in range(5):
        try:
            raw_page = urllib2.urlopen(url).read()
        except:
            continue
        break
    else: #executed if for loop never breaks, i.e. never connects to url
        print "Didn't get {}".format(url)
        return None
    return BeautifulSoup(raw_page)

def getName(sp):
    return sp.select('div#divPGContainer h1.captionText')[0].text

def getPrice(sp):
    tag = sp.select('div#productprice span.price')
    tagOld = sp.select('div#OldPriceForUnavailableProductDiv span')
    if tag:
        price = re.search(PRICE_RE,tag[0].text).group(1)
    elif tagOld:
        price = re.search(PRICEOLD_RE,tagOld[0].text).group(1)
    else:
        price = -999
    return float(price)

def getCategories(sp):
    trivial = ['home','beauty','skin care']
    cats = [cat.text for cat in sp.select('a.breadcrumb') if cat.text not in trivial]
    return cats

def getIngredients(sp):
    tag = sp.select("div#divingredientsPDetail td.contenttd")
    if tag:
        return tag[0].text.split(', ')
    else:
        return []

def getRating(sp):
    tag = sp.select("div.pr-snapshot-rating span.average")
    if tag:
        return float(tag[0].text)
    else:
        return -999.0

def getNReviews(sp):
    tag = sp.select("span.count")
    if tag:
        return int(tag[0].text)
    else:
        return -999
    
def getPros(sp):
    pros = sp.select('div.pr-attribute-pros ul.pr-snapshot-attribute-value-list li')
    return [pro.text for pro in pros]

def getCons(sp):
    cons = sp.select('div.pr-attribute-cons ul.pr-snapshot-attribute-value-list li')
    return [con.text for con in cons]

#Get the list of product urls
mainurl = "http://www.drugstore.com/templates/gn/default.asp?catid=180646&it=5951&"
producturls = []
f = open("product_urls.txt","wb")
for i in xrange(nPages):
    offset = (i+1)*nPerPage
    listurl = mainurl+"&Nao="+str(offset)+"&ipp=72&N=0"
    soup = getsoup(listurl)
    links = soup.select("a.oesLink")
    for link in links:
        if link.find('span')['class'][0] != "verticalFeaturedProductText":
            producturls.append("www.drugstore.com"+link["href"])
            f.write("www.drugstore.com"+link["href"]+"\n")
f.close()

# Getting the info for each product and write to file
# Links to products that fail will be written to another
# file for further investigation.
outfile = open('productJSON.txt', 'wb')
logfile = open('missedproducts.txt','wb')
for prod in producturls[]:
    #print prod
    prodinfo = {}
    soup = getsoup("http://"+prod)
    #print soup
    if soup:
        try:
            prodinfo['name'] = getName(soup)
            prodinfo['price'] = getPrice(soup)
            prodinfo['categories'] = getCategories(soup)
            prodinfo['ingredients'] = getIngredients(soup)
            prodinfo['rating'] = getRating(soup)
            prodinfo['nreviews'] = getNReviews(soup)
            prodinfo['pros'] = getPros(soup)
            prodinfo['cons'] = getCons(soup)
            json_str = json.dumps(prodinfo)
            outfile.write(json_str+'\n')
            #print json_str
            #print "Success."
        except:
            logfile.write(prod+'\n')
            #print "Failed"
    else:
        logfile.write(prod+'\n')
        #pass
logfile.close()
outfile.close()
