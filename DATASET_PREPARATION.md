# Dataset preparation

TerraTorch is a fine-tuning toolkit for Geospatial Foundation Models (GeoFMs). 
It uses PyTorch-Lighting for training, which enables quick fine-tuning of GeoFMs.
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

The data module is responsible for loading all splits in PyTorch-Lighting. It initializes a dataset for each split.
You define the required parameters of the data module in the config which you pass to TerraTorch.
If the parameters are not clearly defined, check the dataset documentation (e.g. `train_split` is passed to the `split` parameter for the train dataset.)

The data parameters are specified in a yaml config, together with other parameters for the model and the training. We explain the config in the workshop.

All generic datasets are loading images and masks with `rioxarray`. You can check if your data is correctly formated by running:

```python
import rioxarray
data = rioxarray.open_rasterio('<example_image_path>', masked=True)
```

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

We provide some example code to prepare the ForestNet dataset in [preprocess_forestnet.py](datasets/preprocess_forestnet.py).
You need to preprocess your dataset in a similar way if you like to use the generic dataset classes. You can run the sample code with:
```shell
python datasets/preprocess_forestnet.py
```

Here is the expected ForestNet dataset structure after the preprocessing.
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


The dataset is represented in the config as follows:

```yaml
data:
  class_path: GenericNonGeoClassificationDataModule
    train_data_root: data/ForestNetDataset/train
    val_data_root: data/ForestNetDataset/val
    test_data_root: data/ForestNetDataset/test
    num_classes: 12
    ...
```

The class indices are based on the alphabetic order of the class names (folder names).

### Scalar Regression
Documentation: [GenericScalarLabelDataset](https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_scalar_label_dataset.GenericScalarLabelDataset)

Single-value regression is currently not supported in a generic DataModule.

### Segmentation
Documentation: [GenericNonGeoSegmentationDataset](https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_pixel_wise_dataset.GenericNonGeoSegmentationDataset)
and [GenericNonGeoSegmentationDataModule](https://ibm.github.io/terratorch/data/#terratorch.datamodules.generic_pixel_wise_data_module.GenericNonGeoSegmentationDataModule)

TerraTorch expects the annotation maps to have a single band with the class indices as values (no RGB class combinations). 
You can place the annotation maps in the same directory and provide `img_grep` and `label_grep` in the config to identify the image-label pairs.
Alternatively, you can store the labels in an extra directory and provide `<split>_label_data_root` additionally to the `<split>_data_root`.
In a third option, you can provide a path to split file with `<split>_split`. The file should contain new-line separated prefixes (substrings) of the samples.

Here is an example of the HLS Burn Scars Dataset structure after running `bash datasets/download_burnscars.sh`. 
```text
MADOS
├── training
│   ├── subsetted_512x512_HLS.S30.T10SDH.2020248.v1.4.mask.tif
│   ├── subsetted_512x512_HLS.S30.T10SDH.2020248.v1.4_merged.tif
│   └── ...
└── validation
    ├── subsetted_512x512_HLS.S30.T10SEH.2018190.v1.4.mask.tif
    ├── subsetted_512x512_HLS.S30.T10SEH.2018190.v1.4_merged.tif
    └── ...
```

With this structure, we define the dataset in the config as follows: 
```yaml
data:
  class_path: GenericNonGeoSegmentationDataModule
    train_data_root: data/HLSBurnScars/training
    val_data_root: data/HLSBurnScars/validation
    img_grep: "*_merged.tif"
    label_grep: "*.mask.tif"
    num_classes: 2
    ...
```

### Pixelwise Regression
Documentation: [GenericNonGeoPixelwiseRegressionDataset](https://ibm.github.io/terratorch/data/#terratorch.datasets.generic_pixel_wise_dataset.GenericNonGeoPixelwiseRegressionDataset)
and [GenericNonGeoPixelwiseRegressionDataModule](https://ibm.github.io/terratorch/data/#terratorch.datamodules.generic_pixel_wise_data_module.GenericNonGeoPixelwiseRegressionDataModule)

The expected data structure is similar to segmentation. Instead of class indices, the label maps represent the ground truth regression values per pixel.

### Torchgeo Datamodule
Documentation: [TorchNonGeoDataModule](https://ibm.github.io/terratorch/data/#terratorch.datamodules.torchgeo_data_module.TorchNonGeoDataModule)
and [TorchGeoDataModule](https://ibm.github.io/terratorch/data/#terratorch.datamodules.torchgeo_data_module.TorchGeoDataModule)

You can use any torchgeo dataset out of the box by using the TerraTorch TorchDataModules.

Here is an example from the [EuroSat config](https://github.com/IBM/terratorch/blob/main/examples/confs/eurosat.yaml) that defines the dataset.

```yaml
data:
  class_path: terratorch.datamodules.TorchNonGeoDataModule
  init_args:
    transforms:
      - class_path: albumentations.augmentations.geometric.resize.Resize
        init_args:
          height: 224
          width: 224
      - class_path: ToTensorV2
    cls: torchgeo.datamodules.EuroSATDataModule
    batch_size: 32
    num_workers: 8
  dict_kwargs:
    root: /dccstor/geofm-pre/EuroSat
    download: True
    bands:
      - B02
      - B03
      - B04
      - B08A
      - B11
      - B12
```

List of all available datasets in torchgeo: https://torchgeo.readthedocs.io/en/stable/api/datamodules.html#non-geospatial-datamodules

### Custom Datamodule

You can write custom scripts for the dataset and data module and refer to the in the config.

```yaml
data:
  class_path: path.to.CustomDataModule
  init_args:
    parameter: value
    ...
```

Check the generic dataset and data module code for inspiration.

## Dataset ideas

You are looking for a dataset that you can use in the workshop?

Check the [torchgeo datasets](https://torchgeo.readthedocs.io/en/stable/api/datamodules.html#non-geospatial-datamodules), as they should work out of the box.

Other dataset collections:
- https://github.com/chrieke/awesome-satellite-imagery-datasets
- https://eod-grss-ieee.com/dataset-search
- https://earthnets.github.io

Ideally, you select a classification, segmentation, or pixel-wise regression dataset with single timestamps, so you can use TerraTorch's generic dataset classes.


## Fine-tuning

Next step: Fine-tuning with [TERRATORCH.md](TERRATORCH.md).