from bs4 import BeautifulSoup as bs
import requests
import re

jeftinije_url = 'https://www.jeftinije.hr/Proizvod/26166528/sportska-oprema-prehrana/satovi-mjeraci-gps/satovi-i-mjeraci/huawei-watch-gt-3-42mm-elegant-gold?ITP=true&MLI=true'
nabava_url = 'https://www.nabava.net/usisavaci/xiaomi-roborock-s7-usisavac-cijena-150552191'

result = requests.get(nabava_url)

doc = bs(result.text, "html.parser")
prices = doc.find_all(text=re.compile(".*€.*"))
# prices2 = doc.find_all("div", class_="offer__price")

print(prices)
clean_prices = []
for price in prices:
    price = price.replace(".", "")
    floaty = float(re.search('[0-9]+.[0-9]*', price).group().replace(',', '.'))
    print(floaty)
    clean_prices.append(floaty)
print(clean_prices)
