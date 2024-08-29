"""
Kikaki, K et al.(2024).
Detecting Marine Pollutants and Sea Surface Features with Deep Learning in Sentinel-2 Imagery.
In ISPRS Journal of Photogrammetry and Remote Sensing.

More information about the dataset: https://marine-pollution.github.io

File names:
*_L2R_cl_*.tif -> semantic class map
*_L2R_conf_*.tif -> class confidence map
*_L2R_rep_*.tif -> unknown (0-1, 1 band, looks similar to confidence)
*_L2R_rgb_*.png -> RGB image
*_L2R_rhorc_*.tif -> Reflectance values of single band (0-1)
"""


import os
import shutil

import tqdm
import warnings
import rasterio as rio
from pathlib import Path
from rasterio.enums import Resampling
warnings.filterwarnings("ignore")

# 16 classes
labels = ['Others', 'Marine Debris', 'Dense Sargassum', 'Sparse Floating Algae', 'Natural Organic Material',
          'Ship', 'Oil Spill', 'Marine Water', 'Sediment-Laden Water', 'Foam', 'Turbid Water', 'Shallow Water',
          'Waves & Wakes', 'Oil Platform', 'Jellyfish', 'Sea snot']


def main():
    data_dir = os.getenv('DATA_DIR', 'data')
    dataset_dir = Path(data_dir) / 'MADOS'

    assert dataset_dir.is_dir(), \
        "Please download the MADOS dataset by running `bash datasets/download_mados.sh`."

    for split in ['train', 'val', 'test']:
        (dataset_dir / split).mkdir(exist_ok=True, parents=True)

        with open(dataset_dir / 'splits' / f'{split}_X.txt', 'r') as f:
            examples = f.read().splitlines()

        # This processing code is based on https://github.com/gkakogeorgiou/mados/blob/master/utils/stack_patches.py
        for example in tqdm.tqdm(examples, mininterval=10):
            scene_name = example.rsplit('_', 1)[0]
            file_pattern = f"{scene_name}_L2R_rhorc_*_{example.split('_')[-1]}.tif"
            # Get the bands for the specific crop
            all_bands = sorted(list(dataset_dir.glob(os.path.join(scene_name, '*', file_pattern))))

            if len(all_bands) != 11:
                print(f'Found missing bands for {example} ({len(all_bands)} bands instead of 11)')
                continue

            # Get metadata from the second 10m band
            with rio.open(all_bands[1], mode = 'r') as src:
                tags = src.tags().copy()
                meta = src.meta
                image = src.read(1)
                shape = image.shape
                dtype = image.dtype

            # Update meta to reflect the number of layers
            meta.update(count=len(all_bands))

            # Stack and save data
            out_file = dataset_dir / split / f'{example}_S2.tif'
            with rio.open(out_file,
                          'w',
                          driver='GTiff',
                          height=shape[-2],
                          width=shape[-1],
                          dtype=dtype,
                          count=len(all_bands),
                          crs='+proj=latlong') as dst:

                for c, band in enumerate(all_bands, 1):
                    upscale_factor = int(os.path.basename(os.path.dirname(band))) // 10

                    with rio.open(band, mode='r') as src:
                        dst.write_band(c, src.read(1,
                                                   out_shape=(
                                                       int(src.height * upscale_factor),
                                                       int(src.width * upscale_factor)
                                                   ),
                                                   resampling=Resampling.nearest
                                                   ).astype(dtype).copy()
                                       )
                dst.update_tags(**tags)

            # Copy annotations *_L2R_cl_*.tif to split dir
            anno_file = dataset_dir / scene_name / '10' / f"{scene_name}_L2R_cl_{example.split('_')[-1]}.tif"
            anno_file_new = dataset_dir / split / f'{example}_annotation.tif'
            _ = shutil.copy(str(anno_file), str(anno_file_new))


if __name__ == '__main__':
    main()
