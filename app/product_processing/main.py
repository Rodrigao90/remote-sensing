import sys

# Check your own path to SNAP-Python
sys.path.append("/home/agostinho/.snap/snap-python")
import snappy
from snappy import GPF
from snappy import ProductIO
from snappy import HashMap


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


def createInterferogram(product_1, product_2):
    """This function creates an interferogram from two products.
    :param product_1: The first product.
    :param product_2: The second product.
    """

    parameters = HashMap()
    parameters.put("subswath", "IW1")  # Specify the desired subswath
    parameters.put("selectedPolarisations", "VV")  # Specify the polarisation
    # specify burst indexes
    parameters.put("selectedBursts", "1")
    product_tops_split_1 = GPF.createProduct(
        "TOPSAR-Split", parameters, product_1
    )
    product_tops_split_2 = GPF.createProduct(
        "TOPSAR-Split", parameters, product_2
    )
    # Appply orbit file
    parameters = HashMap()
    parameters.put("Orbit State Vectors", "Sentinel Precise (Auto Download)")
    parameters.put("Polynomial Degree", "3")
    product_orbit_1 = GPF.createProduct(
        "Apply-Orbit-File", parameters, product_tops_split_1
    )
    product_orbit_2 = GPF.createProduct(
        "Apply-Orbit-File", parameters, product_tops_split_2
    )

    # Co-registration
    correg_product = GPF.createProduct(
        "Coherence", None, product_orbit_1, product_orbit_2
    )
    # Interferogram formation and coherence estimation
    parameters = HashMap()
    parameters.put("Subtract flat-earth phase", "true")
    parameters.put("Degree of 'flat' polynomial", "5")
    parameters.put("Number of 'flat' estimation points", "501")
    parameters.put("Orbit interpolation degree", "3")
    parameters.put("Digital Elevation Model", "SRTM 1Sec HGT")
    parameters.put("Include coherence estimation", "true")
    parameters.put("Square Pixel", "true")
    # Check equation for coherence estimation window size
    parameters.put("Coherence Azimuth Window Size", "10")
    parameters.put("Coherence Range Window Size", "3")
    product_interferogram_1 = GPF.createProduct(
        "Interferogram", parameters, correg_product
    )
    # TOPSAR-Deburst
    parameters = HashMap()
    deburst_product = GPF.createProduct(
        "TOPSAR-Deburst", None, product_interferogram_1
    )
    # GoldsteinPhaseFiltering
    parameters = HashMap()
    filtered_product = GPF.createProduct(
        "GoldsteinPhaseFiltering", None, deburst_product
    )
    return filtered_product


# main
def main():
    # Read products
    file_path_1 = "../copernicus_products/S1A_IW_SLC__1SDV_20170705T075341_20170705T075408_017333_01CF0A_8A21.zip"
    file_path_2 = "../copernicus_products/S1A_IW_SLC__1SDV_20170729T075343_20170729T075410_017683_01D9B6_AB49.zip"
    product_1 = ProductIO.readProduct(file_path_1)
    product_2 = ProductIO.readProduct(file_path_2)
    interferogram = createInterferogram(product_1, product_2)
    # Execute and save
    output_file = "filtered_product.dim"
    ProductIO.writeProduct(interferogram, output_file, "BEAM-DIMAP")


if __name__ == "__main__":
    main()
