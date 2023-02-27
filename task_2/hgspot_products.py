from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def compare(product_link: str, hgspot_price: str, hgspot_des: str):
    
    result              = requests.get(product_link)
    soup                = bs(result.text, "html.parser")
    
    product_name        = soup.find_all( "h1", class_="product-page__title" )[0].text
    offers              = soup.find_all( "div", class_="offer" )
    current_position    = 1
    shops               = []
    hgspot_position     = -1
    position_before_us  = 0
    
    for offer in offers:
        shop_name   = offer.find( "div", class_="offer__store-link" ) ['data-event-label'] .split("-")[1].strip()
        shop_price  = offer.find( "div", class_="offer__price" ).text
        
        shops.append({      'name':     shop_name, 
                            'price':    shop_price, 
                            'position': current_position   
                    })
        
        if shop_name == 'HGSPOT' and hgspot_position == -1:
            hgspot_position = current_position
            if len(shops) >= 1:
                position_before_us = len(shops) 
             
        current_position += 1

    second_place_price  = 0
    third_place_price   = 0
    fourth_place_price  = 0

    min=shops[0]['price']
    max=shops[-1]['price']
    
    if len(shops) >= 4:
        fourth_place_price = shops[3]['price']
    if len(shops) >= 3:
        third_place_price = shops[2]['price']
    if len(shops) >= 2:
        second_place_price = shops[1]['price']
    
    price_before_us = 0
    if position_before_us >= 2:
        price_before_us = shops[position_before_us-2]['price']

    
    product_info={
        "ime proizvoda":                    product_name,
        "hgspot opis proizvoda":            hgspot_des,
        "link proizvoda":                   product_link,
        "hgspot pozicija":                  hgspot_position, 
        "hgspot cijena":                    hgspot_price,
        "cijena ponude prije nas":          price_before_us, 
        "najjeftinija cijena proizvoda":    min, 
        "najskuplja cijena proizvoda":      max, 
        "prva cijena":                      min, 
        "druga cijena":                     second_place_price,
        "treca cijena":                     third_place_price, 
        "cetvrta cijena":                   fourth_place_price, 
    }
    return product_info

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
            product_link        = 'https://www.nabava.net' + product.find( "a", class_="offer__buttons-other-offers" ) [ "href" ]
            
            product_info = compare(product_link, product_price, product_des)

            
            list_of_products.append(product_info)

            
    df = pd.DataFrame(list_of_products)
    # Write the DataFrame to an CSV file
    df.to_csv('output.csv', index=False)

    print(df.head())
    
    # Write the DataFrame to a specific sheet in an Excel file
    # with pd.ExcelWriter('output.xlsx') as writer:
    #   df.to_excel(writer, sheet_name='Sheet1', index=False)
    
main()




   