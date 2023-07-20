from sentinelsat.sentinel import read_geojson, geojson_to_wkt
from main_utils import *
import json



def request_date():
    """This function prompts the user to enter the sensing date information.
    params: .
    """
    year = input('\nInform the year (4 digits): ')
    month = input('Inform the month (2 digits): ')
    day = input('Inform the day (2 digits): ')
    return year + month + day



def request_platform_name():
    """ This function prompts the user to enter the sensing platform name:
    params: .
    """
    platformname = input('\nInform the platform name (Sentinel-1 or Sentinel-2): \n -->')
    return platformname



def request_product_type_S1():
    """ This funtions prompts the user to enter the product type of Sentinel-1
    sensing platform.
    params: .
    """
    producttype = input('\nInform the product type (SLC or GRD): \n --> ')
    return producttype



def request_product_type_S2():
    """ This funtions prompts the user to enter the product type of Sentinel-2
    sensing platform.
    params: .
    """
    producttype = input('\nInform the product type (S2MSI2A or S2MSI1C): \n --> ')
    return producttype



def request_sensor_op_mode():
    """ This funtions prompts the user to enter the sensor operational mode
    of Sentinel-1 sensing platform.
    params: .
    """
    sensor_op_mode = input('\nInform the sensor operational mode (SM, IW, EW, WV): \n --> ')
    return sensor_op_mode



def define_request_json():
    """ This function defines the request json that feeds the query.
    params: .
    """
    clear_screen()
    print('\nInform the initial date: ')
    i_date = request_date()

    clear_screen()
    print('\nInform the final date: ')
    f_date = request_date()

    clear_screen()
    platform_name = request_platform_name()

    if(platform_name == 'Sentinel-1'):
        clear_screen()
        product_type = request_product_type_S1()
        clear_screen()
        sensor_op_mode = request_sensor_op_mode()
    elif(platform_name == 'Sentinel-2'):
        clear_screen()
        product_type = request_product_type_S2()
        clear_screen()
        sensor_op_mode = ' '
    else:
        print("Platform name not identified. Exiting...")
        quit()    

    request_json = {
            'init_date': i_date,
            'final_date': f_date,
            'platform_name': platform_name,
            'product_type' : product_type,
            'sensor_op_mode': sensor_op_mode
            }

    return request_json



def write_request_json(request_json):
    """This function saves in a .json file the information contained in the
    variable request_json.
    params: .
    """
    with open('json/request_json.json', 'w') as outfile:
        json.dump(request_json, outfile)



def read_request_json():
    """This function stores in the variable request_json the information contained in the
    file .json.
    params: .
    """
    with open('json/request_json.json', 'r') as infile:
        return json.load(infile)



def print_query_information(request_json):
    """This function prints the query informaion contained in the variable request_json:
    params: request_json: json containing the query information.
    """
    print("\nPlease, confirm the information provided: ")
    print("\nInitial date: ", request_json['init_date'])
    print("Final date: ", request_json['final_date'])
    print("Platform name: ", request_json['platform_name'])
    print("Product type: ", request_json['product_type'])
    print("Sensor Operational Mode: ", request_json['sensor_op_mode'])



def confirm_information():

    confirmation = input('\n\nIs the information provided correct? (y/n) \n --> ')
    return confirmation.lower()



def confirm_reuse_information():
    confirmation = input('\n\nDo you wish to reuse the previous query? (y/n) \n --> ')
    return confirmation.lower()



def request_query_information():
    c_i = 'n'
    while(c_i == 'n'):
        request_json = define_request_json()
        print_query_information(request_json)
        c_i = confirm_information()

    clear_screen()
    write_request_json(request_json)



def reuse_query_information():
    clear_screen()
    print('Last query used: ')
    try:
        request_json = read_request_json()
        print_query_information(request_json)
        c_r = confirm_reuse_information()
        if(c_r == 'n'):
            request_query_information()
    except:
        request_query_information()



def retrieve_information_from_json(request_json):
    return request_json['init_date'], request_json['final_date'], request_json['platform_name'], request_json['product_type'], request_json['sensor_op_mode']



def get_footprint(geojson_file_address):
    """This function reads the footprint information contained in a geojson file:
    params: geojson_file_address: directory of geojson file containing the footprint information.
    """
    geojson = read_geojson(geojson_file_address)

    return geojson_to_wkt(geojson)



def products_to_dataframe(api, product):
    """This function converts the product resulting from the query into a dataframe.
    params: api: api object.
    params: product: product resulting from the query.
    """
    return api.to_dataframe(product)



def count_products(api,
    footprint,
    date_I,
    date_F,
    platform_name,
    product_type,
    sensor_op_mode):
    """This function counts the products resulting from the query.
    params: api: api object.
    params: footprint: footprint informatio extracted from the geojson file.
    params: date_I: initial sensing date.
    params: date_F: final sensing date.
    params: platform_name: name of the sensing platform.
    params: product_type: name of product type.
    params: sensor_op_mode: sensor operational mode.
    """
    if(sensor_op_mode != ' '): 
        prod_count =  api.count(footprint,
            date=(date_I, date_F),
            platformname=platform_name,
            producttype=product_type,
            sensoroperationalmode=sensor_op_mode,
            relativeorbitnumber=111)
    else:
        prod_count = api.count(footprint,
            date=(date_I, date_F),
            platformname=platform_name,
            producttype=product_type,
            relativeorbitnumber=111)
    
    return prod_count


## Query products in Copernicus Scihub

# Input - API object, initial date, final date, platform name, product type and sensor operational mode
# Output - Dataframe of products and quantity of products

def query_products(api,
    footprint,
    date_I,
    date_F,
    platform_name,
    product_type,
    sensor_op_mode):
    """This function queries the products by using the querying information providade.
    params: api: api object.
    params: footprint: footprint informatio extracted from the geojson file.
    params: date_I: initial sensing date.
    params: date_F: final sensing date.
    params: platform_name: name of the sensing platform.
    params: product_type: name of product type.
    params: sensor_op_mode: sensor operational mode.
    """

    if(sensor_op_mode != ' '):
        products = api.query(footprint,
            date=(date_I, date_F),
            platformname=platform_name,
            producttype=product_type,
            sensoroperationalmode=sensor_op_mode,
            relativeorbitnumber=111)
    else:
        products = api.query(footprint,
            date=(date_I, date_F),
            platformname=platform_name,
            producttype=product_type,
            relativeorbitnumber=111)
        
    return products_to_dataframe(api, products)



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
