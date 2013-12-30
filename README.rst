Project README for pyshopzilla
-------------------------------

Python Library to talk to the Shopzilla Products Search API. Builds queries for comparison results on particular searches.

Sample Usage
============

..code-block:: python

	data = {'apiKey': token, 'publisherId': pubtoken, 'keyword': '',\
        'resultsOffers': 50, 'productId': search_for, 'results': '250'}
    
    # to do - sanitize sarch_string 
    shop = ShopzillaAPI(**data)
    shop.bidded_only()
    shop.contains_images()
    shop.read_response(debug=debug, debug_filename=debug_filename)
    try: 
        shop.parse_json()
    except:
        shop.json_data = shop.response_data

    affiliated_products = shop.json_data
    try: 
        if not affiliated_products.get('products', None):
            affiliated_products = {'products': {'product':[]} }
    except AttributeError:
        affiliated_products = {'products': {'product':[]} }

    counter = 0
    for i in affiliated_products.get('products').get('product'):
        offer_counter = 0
        for offer in i.get('offers').get('offer'):
            try:
                affiliated_products['products']['product'][counter]['offers']['offer'][offer_counter]['short_name'] = str(i['title'][:130])
            except KeyError:
                pass
            offer_counter += 1
        counter += 1

        

Changelog
---------
* 0.1 - Base implementation
* 0.2 - Setuputils and cleanups
* 0.3 - Taxonomy service lookups
* 0.4 - As a module now
