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
    position_before_us = 0
    
    for offer in offers:
        shop_name   = offer.find( "div", class_="offer__store-link" ) ['data-event-label'] .split("-")[1].strip()
        shop_price  = offer.find( "div", class_="offer__price" ).text
        
        shops.append({      'name':     shop_name, 
                            'price':    shop_price, 
                            'position': i   
                    })
        
        if shop_name == 'HGSPOT' and hgspot_position == -1:
            hgspot_position = i 
            position_before_us = len(shops) 
             
        i += 1

    second_place_price  = 0
    third_place_price   = 0
    fourth_place_price  = 0

    position_before_us  = 0
    
    if len(shops) >= 4:
        fourth_place_price = shops[3]['price']
    if len(shops) >= 3:
        third_place_price = shops[2]['price']
    if len(shops) >= 2:
        second_place_price = shops[1]['price']
    
    if position_before_us >= 1:
        position_before_us = shops[position_before_us]['price']
        
    min=shops[0]['price']
    max=shops[-1]['price']
    
    return [ hgspot_position, position_before_us, min, max, second_place_price, third_place_price, fourth_place_price]


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
                                    "ime proizvoda":                    product_des.split(",")[0], 
                                    "hgspot opis proizvoda":            product_des, 
                                    "link proizvoda":                   'https://www.nabava.net' + product_link, 
                                    "hgspot cijena proizvoda":          product_price, 
                                    "hgspot pozicija":                  list[0], 
                                    "cijena ponude prije nas":          list[1],
                                    "najjeftinija cijena proizvoda":    list[2], 
                                    "najskuplja cijena proizvoda":      list[3], 
                                    "prva cijena":                      list[0], 
                                    "druga cijena":                     list[4],
                                    "treca cijena":                     list[5], 
                                    "cetvrta cijena":                   list[6], 
                                    })

            
    df = pd.DataFrame(list_of_products)
    # Write the DataFrame to an CSV file
    df.to_csv('output.csv', index=False)

    print(df.head())
    
    # Write the DataFrame to a specific sheet in an Excel file
    # with pd.ExcelWriter('output.xlsx') as writer:
    #   df.to_excel(writer, sheet_name='Sheet1', index=False)
    
main()




   