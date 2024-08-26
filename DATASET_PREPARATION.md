# Dataset preparation

TerraTorch is a fine-tuning toolkit for Geospatial Foundation Models (GeoFMs). 
It uses PyTorch-Lighting for training, which enables quick fine-tuning of GeoFMs based on a config yaml file.
You find the documentation here: https://ibm.github.io/terratorch/quick_start/.

## Setup

Create venv and install terratorch
```shell
python -m venv venv
source venv/bin/activate
pip install terratorch
```

## Generic dataset classes
TerraTorch comes with some generic dataset classes and data modules. 
If your data is the expected format, you can directly fine-tune a model without any additional Python code.
Alternatively, you can use `torchgeo` data modules or create your custom `Dataset` and `DataModule`.

The datasets are loaded by data modules 

### Classification
Documentation: [GenericNonGeoClassificationDataset](https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_scalar_label_dataset.GenericNonGeoClassificationDataset)
and [GenericNonGeoClassificationDataModule](https://ibm.github.io/terratorch/data/#terratorch.datamodules.generic_scalar_label_data_module.GenericNonGeoClassificationDataModule)

TerraTorch expects the classification samples to be grouped by classes in folders (see [DatasetFolder](https://pytorch.org/vision/main/generated/torchvision.datasets.DatasetFolder.html)).
You can either group the splits by folders or provide additional split files. Each split file should include new-line separated prefixes of the sample paths.   

File structure for samples groups by splits:
```text
DatasetDirectory
├── Split1
│   ├── Class1
│   │   ├── File1
│   │   ├── File2
│   │   ├── ...
│   │   └── FileM
│   ├── Class2
│   ├── ...
│   └── ClassN
├── Split2
│   ├── Class1
│   ├── ...
│   └── ClassN
└── SplitX
    ├── Class1
    ├── ...
    └── ClassN
```


Here is an example for the ForestNet dataset.
```text
ForestNetDataset
├── train
│   ├── Fish pond
│   │   ├── train_153.tif
│   │   ├── train_170.tif
│   │   ├── ...
│   │   └── train_1595.tif
│   ├── Grassland shrubland
│   ├── Logging
│   ├── Mining
│   ├── Oil palm plantation
│   ├── Other
│   ├── Other large-scale plantations
│   ├── Secondary forest
│   ├── Small-scale agriculture
│   ├── Small-scale mixed plantation
│   ├── Small-scale oil palm plantation
│   └── Timber plantation
├── val
│   ├── Fish pond
│   │   ├── val_131.tif
│   │   ├── ...
│   │   └── val_392.tif
│   ├── ...
│   └── Timber plantation
└── test
    ├── Fish pond
    │   ├── test_13.tif
    │   ├── ...
    │   └── test_592.tif
    ├── ...
    └── Timber plantation
```

We provide some example code to prepare the ForestNet dataset in [preprocess_forestnet.py](datasets/preprocess_forestnet.py).
You need to preprocess your dataset in a similar way if you like to use the generic dataset classes.

Config example: TODO

### Scalar Regression 
`GenericScalarLabelDataset`
Documentation: https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_scalar_label_dataset.GenericScalarLabelDataset
Config example: TODO

### Segmentation
`GenericNonGeoSegmentationDataset`
Documentation: https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_pixel_wise_dataset.GenericNonGeoSegmentationDataset
Config example: https://github.com/IBM/terratorch/blob/main/examples/confs/sen1floods11_vit.yaml

### Pixelwise Regression
`GenericNonGeoPixelwiseRegressionDataset`
Documentation: https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_pixel_wise_dataset.GenericNonGeoPixelwiseRegressionDataset
Config example: https://huggingface.co/ibm-granite/granite-geospatial-biomass/blob/main/config.yaml

### Torchgeo Datamodule
`torchgeo.datamodules`
Documentation with list of all available datasets: https://torchgeo.readthedocs.io/en/stable/api/datamodules.html#non-geospatial-datamodules
Config example: https://github.com/IBM/terratorch/blob/main/examples/confs/eurosat.yaml

### Custom Datamodule
TODO