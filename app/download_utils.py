from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from main_utils import *
import json



## Read .txt file containing information (login and password) to access 
## the Copernicus Scihub

# - Input - Empty
# - Output - Login and password

def read_authentication_file():
    with open('authentication.txt') as f:
        login, password = f.readlines()
        return login.strip(), password.strip()



## Authenticate access to the Copernicus Scihub

# Input - Empty
# Output - API object

def authenticate_access():
    login, password = read_authentication_file() 

    return SentinelAPI(login,
            password,
            'https://apihub.copernicus.eu/apihub',
            show_progressbars=True)



def request_date():
    year = input('\nInform year (4 digits): ')
    month = input('Inform month (2 digits): ')
    day = input('Inform day (2 digits): ')
    return year + month + day



def define_request_json():
    clear_screen()
    print('\nInform the initial date: ')
    i_date = request_date()

    clear_screen()
    print('\nInform the final date: ')
    f_date = request_date()

    clear_screen()
    request_json = {
            'init_date': i_date,
            'final_date': f_date,
            'platform_name': 'Sentinel-1',
            'product_type' : 'GRD',
            'sensor_op_mode': 'IW'
            }

    return request_json




def write_request_json(request_json):
    with open('json/request_json.json', 'w') as outfile:
        json.dump(request_json, outfile)



def read_request_json():
    with open('json/request_json.json', 'r') as infile:
        return json.load(infile)



def check_query_information(request_json):
    print("\nPlease, confirm the information provided: ")
    print("\nInitial date: ", request_json['init_date'])
    print("Final date: ", request_json['final_date'])
    print("Platform name: ", request_json['platform_name'])
    print("Product type: ", request_json['product_type'])
    print("Sensor Operational Mode: ", request_json['sensor_op_mode'])



def confirm_information():
    confirmation = input('\n\nIs the information provided correct? (y/n)')
    return confirmation.lower()



def confirm_reuse_information():
    confirmation = input('\n\nDo you wish to reuse the previous query? (y/n)')
    return confirmation.lower()



def request_query_information():
    c_i = 'n'
    while(c_i == 'n'):
        request_json = define_request_json()
        check_query_information(request_json)
        c_i = confirm_information()

    clear_screen()
    write_request_json(request_json)



def reuse_query_information():
    clear_screen()
    print('Last query used: ')
    try:
        request_json = read_request_json()
        check_query_information(request_json)
        c_r = confirm_reuse_information()
        if(c_r == 'n'):
            request_query_information()
    except:
        request_query_information()



def retrieve_information_from_json(request_json):
    return request_json['init_date'], request_json['final_date'], request_json['platform_name'], request_json['product_type'], request_json['sensor_op_mode']


## Get footprint from GeoJSON file

# Input - File .geojson of area of interest
# Output - Footprint of area of interest

def get_footprint(geojson_file_address):
    geojson = read_geojson(geojson_file_address)

    return geojson_to_wkt(geojson)



## Organize products in a dataframe structure

# Input - API object and query of Products
# Output - Dataframe of products

def products_to_dataframe(api, product):

    return api.to_dataframe(product)



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
    
    footprint = get_footprint('geojson/map.geojson')

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
    API.download(product_ID, "products/")



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
