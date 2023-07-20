from glob import glob
import snappy
from snappy import GPF, ProductIO, HashMap



def retrieve_products_from_satellite(sat):
    list_of_files = glob('products/S1*')
    for f in list_of_files:
        print(f)



def createProduct(operation_name, product_1, product_2=None, parameters=None):
    """This function creates a product from a given operation name and parameters.
    :param operation_name: The name of the operation.
    :param product_1: The first product.
    :param product_2: The second product.
    :param parameters: The parameters.
    """
    if product_2:
        return GPF.createProduct(
            operation_name, parameters, product_1, product_2
        )
    else:
        return GPF.createProduct(operation_name, parameters, product_1)

