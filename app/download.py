from download_utils import *
from main_utils import *


## Define search parameters

reuse_query_information()

r_json = read_request_json()

date_i, date_f, platform_name, product_type, sensor_op_mode = retrieve_information_from_json(r_json)



## Authentication

api = authenticate_access()

products_df, count = query(api, 
        date_i,
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
