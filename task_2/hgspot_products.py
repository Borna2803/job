from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


def compare(product_link: str):
    nabava_url      = 'https://www.nabava.net'
    result          = requests.get(nabava_url+product_link)
    soup            = bs(result.text, "html.parser")
    offers          = soup.find_all("div", class_="offer")
    i               = 1
    shops           = []
    hgspot_position = -1
    
    for offer in offers:
        shop_name   = offer.find( "div", class_="offer__store-link" ) ['data-event-label'] .split("-")[1].strip()
        shop_price  = offer.find( "div", class_="offer__price" ).text
        
        shops.append({      'name':     shop_name, 
                            'price':    shop_price, 
                            'position': i   
                    })

        if shop_name=='HGSPOT':
            hgspot_position=i
        i+=1

    min=shops[0]['price']
    max=shops[-1]['price']
    return [min, max, hgspot_position]




def main():

    hgspot_url          = 'https://www.nabava.net/hgspot/ponuda?s='
    list_of_products    = []
    n                   = 134

    #izbrisi ovo
    n=2


    for i in range(1, n):
        url         = hgspot_url + str(i)
        result      = requests.get(url)
        soup        = bs( result.text, "html.parser" )
        products    = soup.find_all( "div", class_="offer" )

        for product in products:
            product_des         = product.find("div", class_="offer__name").text
            product_price       = product.find("div", class_="offer__price").text
            product_link        = product.find( "a", class_="offer__buttons-other-offers" ) [ "href" ]
            
            list = compare(product_link)
            
            list_of_products.append({   
                                    "product name":     product_des.split(",")[0], 
                                    "hgspot description":      product_des, 
                                    "product link":     'https://www.nabava.net' + product_link, 
                                    "hgspot price":    product_price, 
                                    "min":              list[0], 
                                    "max":              list[1],
                                    "hgspot position":         list[2], 
                                    })
            
    df = pd.DataFrame(list_of_products)
    print(df.head())

main()
   