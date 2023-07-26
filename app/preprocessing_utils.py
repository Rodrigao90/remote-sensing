import os
import snappy
from snappy import GPF
from snappy import ProductIO
from snappy import HashMap
from snappy import jpy
import subprocess
from time import *

# documentation: http://step.esa.int/docs/v2.0/apidoc/engine/overview-summary.html

print('snappy.__file__:', snappy.__file__)
# prints the path to the snappy configs.
#change in jpyconfig.py e.g. jvm_maxmem = '30G' and in snappy.ini java_max_mem: 30G (and uncomment)

swath = 'IW1'
output= 'test.dim'

# Hashmap is used to give us access to all JAVA oerators
HashMap = jpy.get_type('java.util.HashMap')
parameters = HashMap()

def read(filename):
    return ProductIO.readProduct(filename)

def write(product, filename):
    ProductIO.writeProduct(product, filename, "BEAM-DIMAP")
    # Allowed formats to write: GeoTIFF-BigTIFF,HDF5,Snaphu,BEAM-DIMAP,
        # GeoTIFF+XML,PolSARPro,NetCDF-CF,NetCDF-BEAM,ENVI,JP2,
    # Generic Binary BSQ,Gamma,CSV,NetCDF4-CF,GeoTIFF,NetCDF4-BEAM


def topsar_split(product):
    parameters.put('subswath', "IW1")
    parameters.put('selectedPolarisations', 'VV')
    parameters.put("selectedBursts", "1")
    return GPF.createProduct("TOPSAR-Split", parameters, product)

def apply_orbit_file(product):
    parameters.put("Orbit State Vectors", "Sentinel Precise (Auto Download)")
    parameters.put("Polynomial Degree", 3)
    return GPF.createProduct("Apply-Orbit-File", parameters, product)

def back_geocoding(product):
    parameters.put("Digital Elevation Model", "SRTM 1Sec HGT (Auto Download)")
    parameters.put("DEM Resampling Method", "BICUBIC_INTERPOLATION")
    parameters.put("Resampling Type", "BISINC_5_POINT_INTERPOLATION")
    parameters.put("Mask out areas with no elevation", True)
    parameters.put("Output Deramp and Demod Phase", False)
    return GPF.createProduct("Back-Geocoding", parameters, product)


def interferogram(product):
    parameters.put("Subtract flat-earth phase", True)
    parameters.put("Degree of \"Flat Earth\" polynomial", 5)
    parameters.put("Number of \"Flat Earth\" estimation points", 501)
    parameters.put("Orbit interpolation degree", 3)
    parameters.put("Include coherence estimation", True)
    parameters.put("Square Pixel", False)
    parameters.put("Independent Window Sizes", False)
    parameters.put("Coherence Azimuth Window Size", 10)
    parameters.put("Coherence Range Window Size", 10)
    return GPF.createProduct("Interferogram", parameters, product)

def topsar_deburst(product):
    parameters.put("Polarisations", "VV")

def topophase_removal(product):
    parameters.put("Orbit Interpolation Degree", 3)
    parameters.put("Digital Elevation Model", "SRTM 1Sec HGT (Auto Download)")
    parameters.put("Tile Extension[%]", 100)
    parameters.put("Output topographic phase band", True)
    parameters.put("Output elevation band", False)
    return GPF.createProduct("TopoPhaseRemoval", parameters, product)


def goldstein_phasefiltering(product):
    parameters.put("Adaptive Filter Exponent in(0,1]:", 1.0)
    parameters.put("FFT Size", 64)
    parameters.put("Window Size", 3)
 U  parameters.put("Use coherence mask", False)
    parameters.put("Coherence Threshold in[0,1]:", 0.2)
    return GPF.createProduct("GoldsteinPhaseFiltering", parameters, product)

def write_snaphu(product, filename):
    ProductIO.writeProduct(product, filename, "Snaphu")

def insar_pipeline(filename_1, filename_2):

    print('Reading SAR data')
    product_1 = read(filename_1)
    product_2 = read(filename_2)

    print('TOPSAR-Split')
    product_TOPSAR_1 = topsar_split(product_1)
    product_TOPSAR_2 = topsar_split(product_2)

    print('Applying precise orbit files')
    product_orbitFile_1 = apply_orbit_file(product_TOPSAR_1)
    product_orbitFile_2 = apply_orbit_file(product_TOPSAR_2)

    print('back geocoding')
    backGeocoding = back_geocoding([product_orbitFile_1, product_orbitFile_2])

    print('inerferogram generation')
    interferogram_formation = interferogram(backGeocoding)

    print('TOPSAR_deburst')
    TOPSAR_deburst = topsar_deburst(interferogram_formation)

    print('TopoPhase removal')
    TOPO_phase_removal = topophase_removal(TOPSAR_deburst)

    print('Goldstein filtering')
    goldstein_phasefiltering(TOPO_phase_removal)

    print('Writing (only) final product')
    write(TOPO_phase_removal, output)
    # the next one is a timewaste, as it produces only snaphu configs and hdr, this still is done better in
    # the GUI...
    write_snaphu(TOPO_phase_removal, 'snaphu')

