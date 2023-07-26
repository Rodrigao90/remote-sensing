import sys

# Check your own path to SNAP-Python
sys.path.append("/home/agostinho/.snap/snap-python")
import snappy
from snappy import GPF
from snappy import ProductIO
from snappy import HashMap


def createInterferogram(product_1, product_2, stage=None):
    """This function creates an interferogram from two products up to a certain stage.
    :param product_1: The first product.
    :param product_2: The second product.
    :param stage: The processing stage to stop at.
    """

    stage_operations = {
        "split": {
            "operator": "TOPSAR-Split",
            "parameters": {
                "subswath": "IW1",
                "selectedPolarisations": "VV",
                "selectedBursts": "1",
            },
            "is_dual": True,
        },
        "orbit": {
            "operator": "Apply-Orbit-File",
            "parameters": {
                "Orbit State Vectors": "Sentinel Precise (Auto Download)",
                "Polynomial Degree": "3",
            },
            "is_dual": True,
        },
        "coregistration": {
            "operator": "Coherence",
            "parameters": {},
            "is_dual": False,
        },
        "interferogram": {
            "operator": "Interferogram",
            "parameters": {
                "Subtract flat-earth phase": "true",
                "Degree of 'flat' polynomial": "5",
                "Number of 'flat' estimation points": "501",
                "Orbit interpolation degree": "3",
                "Digital Elevation Model": "SRTM 1Sec HGT",
                "Include coherence estimation": "true",
                "Square Pixel": "true",
                "Coherence Azimuth Window Size": "10",
                "Coherence Range Window Size": "3",
            },
            "is_dual": False,
        },
        "deburst": {
            "operator": "TOPSAR-Deburst",
            "parameters": {},
            "is_dual": False,
        },
        "filter": {
            "operator": "GoldsteinPhaseFiltering",
            "parameters": {},
            "is_dual": False,
        },
    }

    if stage is not None and stage not in stage_operations:
        raise ValueError(
            f"Invalid stage. Expected one of: {list(stage_operations.keys())}"
        )

    product_a, product_b = product_1, product_2

    for stage_name, operation in stage_operations.items():
        params = HashMap()
        for key, value in operation["parameters"].items():
            params.put(key, value)

        if operation["is_dual"]:
            product_a = GPF.createProduct(
                operation["operator"], params, product_a
            )
            product_b = GPF.createProduct(
                operation["operator"], params, product_b
            )
            result = (product_a, product_b)
        else:
            if stage_name == "coregistration":
                result = GPF.createProduct(
                    operation["operator"], params, product_a, product_b
                )
            else:
                result = GPF.createProduct(
                    operation["operator"], params, result
                )

        if stage_name == stage:
            break

    return result


# main
def main():
    # Read products
    file_path_1 = "../copernicus_products/S1A_IW_SLC__1SDV_20170705T075341_20170705T075408_017333_01CF0A_8A21.zip"
    file_path_2 = "../copernicus_products/S1A_IW_SLC__1SDV_20170729T075343_20170729T075410_017683_01D9B6_AB49.zip"

    product_1 = ProductIO.readProduct(file_path_1)
    product_2 = ProductIO.readProduct(file_path_2)
    interferogram = createInterferogram(product_1, product_2, stage="filter")
    # Execute and save
    output_file = "filtered_product.dim"
    ProductIO.writeProduct(interferogram, output_file, "BEAM-DIMAP")


if __name__ == "__main__":
    main()
