from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
import os



## Read .txt file containing information (login and password) to access 
## the Copernicus Scihub

# - Input - ?
# - Output - Login and password

def read_authentication_file():
    with open('authentication.txt') as f:
        login, password = f.readlines()
        return login.strip(), password.strip()



## Authenticate access to the Copernicus Scihub

# Input - ?
# Output - API object

def authenticate():
        
    login, password = read_authentication_file() 

    return SentinelAPI(login,
            password,
            'https://apihub.copernicus.eu/apihub',
            show_progressbars=True)



## Get footprint from GeoJSON file

# Input - File .geojson of area of interest
# Output - Footprint of area of interest

def get_footprint(geojson_file):

    geojson = read_geojson(geojson_file)

    return geojson_to_wkt(geojson)



## Organize products in a dataframe structure

# Input - API object and query of Products
# Output - Dataframe of products

def products_to_dataframe(api, products):

    return api.to_dataframe(products)



## Count products queried

# Input - Footprint, Initial date, final date, platform name, product type and sensor operational mode
# Output - Number of products

def count_products(api,
    footprint,
    date_I,
    date_F,
    platform_name,
    product_type,
    sensor_op_mode):

    return api.count(footprint,
        date=(date_I, date_F),
        platformname=platform_name,
        producttype=product_type,
        sensoroperationalmode=sensor_op_mode)



## Query products in Copernicus Scihub

# Input - API object, initial date, final date, platform name, product type and sensor operational mode
# Output - Dataframe of products and quantity of products

def query(api,
    date_I,
    date_F,
    platform_name,
    product_type,
    sensor_op_mode):
    
    footprint = get_footprint('../geojson/map.geojson')

    prod_count = count_products(api,
        footprint,
        date_I,
        date_F,
        platform_name,
        product_type,
        sensor_op_mode)
    
    if prod_count > 1:
        print(str(prod_count) + " products found!")
        products = api.query(footprint,
            date=(date_I, date_F),
            platformname=platform_name,
            producttype=product_type,
            sensoroperationalmode=sensor_op_mode)

        return products_to_dataframe(api, products), prod_count

    print("No product found!")
    print("End!")
    exit()



def check_availability(API, product_ID):
    return API.is_online(product_ID)  



def download_file(API, product_ID):
    API.download(product_ID, "../products/")



def trigger_offline_retrieval(API, product_ID):
    API.trigger_offline_retrieval(product_ID)



def get_products_NAMES_list(products_DF):
    return products_DF['filename'].values



def get_products_IDS_list(products_DF):
    return products_DF['uuid'].values



def check_and_download_products(API,
                                products_NAMES_list,
                                products_IDS_list,
                                prod_count):

    for i in range(prod_count):
    
        product_NAME = products_NAMES_list[i]
        product_ID = products_IDS_list[i]

        file_path = "products/" + product_NAME.replace('.SAFE', '.zip')
            
        if os.path.isfile(file_path):
            print("File " + str(i) + " exists!")
        else:
            print("File " + str(i) + " does not exist!")
            if check_availability(API, product_ID):
                print("The file is available to be downloaded!")
                print("Starting download...")
                download_file(API, product_ID)
            else:
                print("The file is NOT available to be downloaded!")
                trigger_offline_retrieval(API, product_ID)
                print("The file has been requested!")