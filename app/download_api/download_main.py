from download_utils import *
from datetime import date
import os


## Define search parameters

geojson_file = '../geojson/map.geojson'

date_i = date(2022, 5, 20)
date_f = date(2022, 6, 6)

platform_name = 'Sentinel-1'
product_type = 'GRD'
sensor_op_mode = 'IW'


## Authentication

api = authenticate()

products_df, count = query(api,date_i,
        date_f,
        platform_name,
        product_type,
        sensor_op_mode)

products_names_list = get_products_NAMES_list(products_df)
products_ids_list = get_products_IDS_list(products_df)

check_and_download_products(api,
                            products_names_list,
                            products_ids_list,
                            count)
    
print("End!")