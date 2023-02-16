def best_option(delivery_services: list) -> dict:
    min = delivery_services[0]['price']
    tmp = delivery_services[0]
    for delivery_service in delivery_services:
        if delivery_service['price'] < min:
            min = delivery_service['price']
            tmp = delivery_service
    return tmp
 
def parcel_delivery(packages: list, package_options: list, additional_weight: float, additional_price: float )-> dict:
    
    weight_of_packages=0.0
    for package in packages:
        weight_of_packages += package['weight'] * package['count']

    for package_option in package_options:
        if weight_of_packages <= package_option['weight']:
            return { 'price' : package_option['price'], 'packages': [{ 'weight' : package_option['weight'], 'count' : 1 }]}

    max_available_package_option = package_options[-1]['weight']
    max_available_package_cost  = package_options[-1]['price']
    
    weight_of_packages -= max_available_package_option
    weight_option=max_available_package_option
    delivery_price=max_available_package_cost
    iteration = 0

    while weight_of_packages > 0.0:
        weight_of_packages -= additional_weight
        weight_option += additional_weight
        delivery_price += additional_price  
        iteration += 1

    return {'price' : delivery_price, 'packages': [{ 'weight' : max_available_package_option, 'count' : 1}, { 'weight' : additional_weight, 'count' : iteration }]}

 
def package_delivery( packages:list, options:list ) -> dict:
    delivery_price = 0.0
    package_counter = {}
    for option in options:
        package_counter[option['weight']]= 0

    for package in packages:
        for option in options:
            if package['weight'] <= option['weight']:
                package_counter[option['weight']] += package['count']
                delivery_price += float(package['count']*option['price'])
                break

    package_delivery = []
    for package_weight, package_count in package_counter.items():
        if package_count > 0:
            package_delivery.append({ 'weight' : package_weight, 'count' : package_count })
        
    return { 'price' : delivery_price,  'packages': package_delivery }


def delivery_cost( packages:list, otok = False, bijela_tehnika = False ) -> dict:

    overweight=False
    for package in packages:
        if package['weight'] > 30:
            overweight=True
    
    if bijela_tehnika:
        if otok:
            intime_zone2 = parcel_delivery(packages, intime_data_zone2, intime_additional_weight, intime_additional_price_zone2)
            return {
            "name": "intime",
            "type": "parcel",
            "price": intime_zone2['price'],
            "package_option": intime_zone2['packages']
        }
        intime = parcel_delivery(packages, intime_data, intime_additional_weight, intime_additional_price)
        return {
            "name": "intime",
            "type": "parcel",
            "price": intime['price'],
            "package_option": intime['packages']
        }
    elif overweight:
        if otok:
            overseas = parcel_delivery( packages, overseas_data, overseas_additional_weight, overseas_additional_price)
            intime_zone2 = parcel_delivery(packages, intime_data_zone2, intime_additional_weight, intime_additional_price_zone2)
            list_of_options = [
            {
                "name": "overseas",
                "type": "parcel",
                "price": overseas['price'],
                "package_options": overseas['packages']
            },
            {
                "name": "intime",
                "type": "parcel",
                "price": intime_zone2['price'],
                "package_option": intime_zone2['packages']
            }]
            return best_option(list_of_options)
       
        overseas = parcel_delivery( packages, overseas_data, overseas_additional_weight, overseas_additional_price)
        intime = parcel_delivery(packages, intime_data, intime_additional_weight, intime_additional_price)
        list_of_options = [
        {
            "name": "overseas",
            "type": "parcel",
            "price": overseas['price'],
            "package_options": overseas['packages']
        },
        {
            "name": "intime",
            "type": "parcel",
            "price": intime['price'],
            "package_option": intime['packages']
        }]
        return best_option(list_of_options)

        
        
    elif otok :
        hp = package_delivery(packages, hp_data)
        return {
            "name": "intime",
            "type": "parcel",
            "price": hp['price'],
            "package_option": hp['packages']
        }

    overseas = parcel_delivery( packages, overseas_data, overseas_additional_weight, overseas_additional_price)
    intime = parcel_delivery(packages, intime_data, intime_additional_weight, intime_additional_price)
    hp = package_delivery(packages, hp_data)
    gls = package_delivery(packages, gls_data)
    
    list_of_options = [
        {
            "name": "overseas",
            "type": "parcel",
            "price": overseas['price'],
            "package_options": overseas['packages']
        },
        {
            "name": "intime",
            "type": "parcel",
            "price": intime['price'],
            "package_option": intime['packages']
        },
        {
            "name": "hp",
            "type": "package",
            "price": hp['price'],
            "package_option": hp['packages']
        },
        {
            "name": "gls",
            "type": "package",
            "price": gls['price'],
            "package_option": gls['packages']
        }
    ]
    return best_option(list_of_options)


hp_data=[   
    {'weight': 1.0, 'price': 2.1236}, 
    {'weight': 2.0, 'price': 2.2563}, 
    {'weight': 5.0, 'price': 2.4554}, 
    {'weight': 10.0, 'price': 2.6545}, 
    {'weight': 15.0, 'price': 2.9199}, 
    {'weight': 20.0, 'price': 3.4508}, 
    {'weight': 30.0, 'price': 4.1144}]

gls_data = [
    {'weight': 2.0, 'price': 3.26}, 
    {'weight': 3.0, 'price': 3.47}, 
    {'weight': 5.0, 'price': 3.68}, 
    {'weight': 10.0, 'price': 3.97}, 
    {'weight': 15.0, 'price': 4.25}, 
    {'weight': 20.0, 'price': 4.46}, 
    {'weight': 25.0, 'price': 4.75},
    {'weight': 30.0, 'price': 5.03}, 
    {'weight': 40.0, 'price': 5.45}]

overseas_data = [
    {'weight': 2.0, 'price': 2.9038}, 
    {'weight': 5.0, 'price': 3.6298}, 
    {'weight': 10.0, 'price': 3.9525}, 
    {'weight': 15.0, 'price': 4.2751}, 
    {'weight': 20.0, 'price': 4.5171}, 
    {'weight': 25.0, 'price': 5.0011}, 
    {'weight': 30.0, 'price': 6.1303}, 
    {'weight': 35.0, 'price': 9.0342}, 
    {'weight': 40.0, 'price': 10.3248}, 
    {'weight': 45.0, 'price': 10.9701}, 
    {'weight': 50.0, 'price': 12.906}, 
    {'weight': 80.0, 'price': 15.8098}, 
    {'weight': 100.0, 'price': 18.875}, 
    {'weight': 150.0, 'price': 22.4241}, 
    {'weight': 200.0, 'price': 34.6848}, 
    {'weight': 250.0, 'price': 40.0085}, 
    {'weight': 300.0, 'price': 43.5576}, 
    {'weight': 350.0, 'price': 45.9775}, 
    {'weight': 400.0, 'price': 51.6239}, 
    {'weight': 450.0, 'price': 51.6239}, 
    {'weight': 500.0, 'price': 60.4967}]
overseas_additional_weight = 1
overseas_additional_price = 0.1247

intime_data = [
    {'weight': 2, 'price': 2.7474},
    {'weight': 5, 'price': 2.7474},
    {'weight': 10, 'price': 3.0526},
    {'weight': 15, 'price': 3.2053},
    {'weight': 20, 'price': 3.5868},
    {'weight': 25, 'price': 4.0447},
    {'weight': 30, 'price': 4.6553},
    {'weight': 35, 'price': 5.2841},
    {'weight': 40, 'price': 5.8702},
    {'weight': 45, 'price': 14.6755},
    {'weight': 50, 'price': 14.6755},
    {'weight': 60, 'price': 14.6755},
    {'weight': 70, 'price': 14.6755},
    {'weight': 80, 'price': 22.014},
    {'weight': 90, 'price': 22.014},
    {'weight': 100, 'price': 22.014},
    {'weight': 150, 'price': 29.3525},
    {'weight': 200, 'price': 32.2876},
    {'weight': 250, 'price': 36.6895},
    {'weight': 300, 'price': 44.028},
    {'weight': 350, 'price': 51.3665},
    {'weight': 400, 'price': 58.705},
    {'weight': 450, 'price': 66.042},
    {'weight': 500, 'price': 73.3805},
    {'weight': 600, 'price': 88.056},
    {'weight': 700, 'price': 102.733},
    {'weight': 800, 'price': 117.4085},
    {'weight': 900, 'price': 132.084},
    {'weight': 1000, 'price': 146.761},
    {'weight': 1500, 'price': 220.1415},
    {'weight': 2000, 'price': 293.6396},
    {'weight': 2500, 'price': 366.9026},
    {'weight': 3000, 'price': 440.2831}]

intime_data_zone2 = [
    {'weight': 2, 'price': 3.567},
    {'weight': 5, 'price': 3.7639},
    {'weight': 10, 'price': 3.9623},
    {'weight': 15, 'price': 4.3591},
    {'weight': 20, 'price': 4.7545},
    {'weight': 25, 'price': 5.5481},
    {'weight': 30, 'price': 6.3403},
    {'weight': 35, 'price': 7.1325},
    {'weight': 40, 'price': 7.9246},
    {'weight': 45, 'price': 19.8131},
    {'weight': 50, 'price': 19.8131},
    {'weight': 60, 'price': 19.8131},
    {'weight': 70, 'price': 19.8131},
    {'weight': 80, 'price': 29.7188},
    {'weight': 90, 'price': 29.7188},
    {'weight': 100, 'price': 29.7188},
    {'weight': 150, 'price': 39.6261},
    {'weight': 200, 'price': 43.5884},
    {'weight': 250, 'price': 49.5319},
    {'weight': 300, 'price': 59.4377},
    {'weight': 350, 'price': 69.3449},
    {'weight': 400, 'price': 79.2507},
    {'weight': 450, 'price': 89.1565},
    {'weight': 500, 'price': 99.0638},
    {'weight': 600, 'price': 118.8768},
    {'weight': 700, 'price': 138.6884},
    {'weight': 800, 'price': 158.5014},
    {'weight': 900, 'price': 178.3145},
    {'weight': 1000, 'price': 198.1275},
    {'weight': 1500, 'price': 297.1913},
    {'weight': 2000, 'price': 396.2536},
    {'weight': 2500, 'price': 495.3173},
    {'weight': 3000, 'price': 594.3811}]
intime_additional_weight = 500.0
intime_additional_price = 73.3805
intime_additional_price_zone2 = 99.0638


def test():
    #general test
    test = [
        {'weight': 20.0, 'count': 6},
        {'weight': 30.0, 'count': 2},
        {'weight': 16.3, 'count': 2},
        {'weight': 20.2, 'count': 6},
    ]

    #razlika između drugog i trećeg testa nam pokazuje kako se za VIŠE PROIZVODA MALE KILAŽE više isplati koristiti služba
    #kao intime koji funkcioniraju na način 'pošiljke' (tj. svi paketi se zbrajaju i šalju ko jedan paket) dok se za 
    #MANJE PROIZVODA MALE vise isplati koristiti služba kao hp koja koristi način 'paket' 
    #(tj. svakom paketu se gleda zasebna masa, traži se prikladna veličina i na temelju toga se formira cijena)

    test2 = [
        {'weight': 0.8, 'count': 15},

    ]
    test3 = [
        {'weight': 0.8, 'count': 1},
    ]

    #razlika između trećeg i četvrtog testa nam pokazuje kako se za VIŠE PROIZVODA VELIKE KILAŽE više isplati koristiti služba
    #kao overseas koji funkcioniraju na način 'pošiljke' (tj. svi paketi se zbrajaju i šalju ko jedan paket) dok se za 
    #MANJE PROIZVODA VELIKE vise isplati koristiti služba kao hp koja koristi način 'paket' 
    #(tj. svakom paketu se gleda zasebna masa, traži se prikladna veličina i na temelju toga se formira cijena)
    test4 = [
        {'weight': 20, 'count': 15},
    ]
    test5 = [
        {'weight': 20, 'count': 1},
    ]

    print(delivery_cost(test))
    print(delivery_cost(test2))
    print(delivery_cost(test3))
    print(delivery_cost(test4))
    print(delivery_cost(test5))