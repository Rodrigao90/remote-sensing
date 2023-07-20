from download_utils import *
from main_utils import *
from authentication import *


## Define search parameters

reuse_query_information()
r_json = read_request_json()
date_i, date_f, platform_name, product_type, sensor_op_mode = retrieve_information_from_json(r_json)


## Authentication

api = authenticate_access('authentication_file.txt')


## Query

footprint = get_footprint('geojson/map.geojson')

products_count = count_products(api,
        footprint,
        date_i,
        date_f,
        platform_name,
        product_type,
        sensor_op_mode)

if products_count > 1:
    print(str(products_count) + " products found!")
    
    products_df = query_products(api,
            footprint,
            date_i,
            date_f,
            platform_name,
            product_type,
            sensor_op_mode)
else:
    print("No enough products found!")
    print("End!")
    exit()

products_names_list = get_products_NAMES_list(products_df)
products_ids_list = get_products_IDS_list(products_df)

check_and_download_products(api,
                            products_names_list,
                            products_ids_list,
                            products_count)
    
print("End!")
