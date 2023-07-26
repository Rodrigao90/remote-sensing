from preprocessing_utils_2 import *

master  = "products/S1A_IW_SLC__1SDV_20220516T075409_20220516T075436_043233_0529C8_8873.zip"

slave = "products/S1A_IW_SLC__1SDV_20220528T075410_20220528T075437_043408_052EF7_4F2C.zip"

swath = 'IW1'
output= 'test.dim'


insar_pipeline(master, slave)

#seperate snaphu writeout (this is very stupid... but if you writeout as snaphu it does not writeout the phase and coherence)
source_product_path = os.path.join(output)
source_product = read(source_product_path)
target_product = snappy.Product(source_product.getName(),
        source_product.getProductType(),
        source_product.getSceneRasterWidth(),
        source_product.getSceneRasterHeight())

target_product_path = os.path.join('snaphu')
for source_band in source_product.getBands():
    band_name = source_band.getName()
    if band_name.startswith('coh'):
        ProductUtils.copyBand(band_name, source_product, target_product, True)
        write(target_product, target_product_path)
    elif band_name.startswith('Phase'):
        ProductUtils.copyBand(band_name, source_product, target_product, True)
        write(target_product, target_product_path)

