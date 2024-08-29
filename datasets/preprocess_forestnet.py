"""
Irvin, J et al.(2020).
ForestNet: Classifying Drivers of Deforestation in Indonesia using Deep Learning on Satellite Imagery.
In NeurIPS 2020 workshop on Tackling Climate Change with Machine Learning.

More information about the dataset: https://stanfordmlgroup.github.io/projects/forestnet/
"""

import os
import tqdm
import warnings
import pandas as pd
import numpy as np
import rasterio as rio
from pathlib import Path
warnings.filterwarnings("ignore")


def main():
    data_dir = os.getenv('DATA_DIR', 'data')
    dataset_dir = Path(data_dir) / 'ForestNetDataset'

    assert dataset_dir.is_dir(), \
        "Please download the ForestNetDataset by running `bash datasets/download_forestnet.sh`."

    default_transform = rio.transform.from_bounds(0, 0, 332, 332, width=332, height=332)

    for split in ['train', 'val', 'test']:
        examples = pd.read_csv(dataset_dir / f'{split}.csv')

        # Create class dirs
        # Expected structure by the TerraTorch generic classification dataset, see:
        # from terratorch.datasets import GenericNonGeoClassificationDataset
        # from terratorch.datamodules import GenericNonGeoClassificationDataModule
        class_names = examples['label'].unique()
        for class_name in class_names:
            (dataset_dir / split / class_name).mkdir(exist_ok=True, parents=True)

        for i, row in tqdm.tqdm(examples.iterrows(), total=len(examples), desc=split, maxinterval=10):
            # Load RGB and IR files
            rgb_file = dataset_dir / row['example_path'] / 'images' / 'visible' / 'composite.png'
            ir_file = dataset_dir / row['example_path'] / 'images' / 'infrared' / 'composite.npy'
            if not rgb_file.exists() or not ir_file.exists():
                print(f"Missing {row['example_path']}")
                continue

            with rio.open(rgb_file) as src:
                rgb = src.read()
            ir = np.load(ir_file)

            # Stack bands (to match Prithvi channels)
            # BLUE, GREEN, RED, NIR_NARROW, SWIR_1, SWIR_2 / Landsat: B02, B03, B04, B05, B06, B07
            # Note that you don't have to match the channels, you can also define them in the config.
            stacked = np.concatenate([rgb[[2, 1, 0]], ir.transpose((2, 0, 1))], axis=0)

            # Save images in dedicated folder per class
            out_file = dataset_dir / split / row['label'] / f'{split}_{i}.tif'
            with rio.open(out_file,
                          'w',
                          driver='GTiff',
                          height=332,
                          width=332,
                          dtype=stacked.dtype,
                          transform=default_transform,  # Adding wrong geotransform to avoid NotGeoreferencedWarning
                          count=6) as dst:
                dst.write(stacked)


if __name__ == '__main__':
    main()
