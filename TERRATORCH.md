# TerraTorch

TerraTorch is a fine-tuning toolkit for Geospatial Foundation Models (GeoFMs). 
It uses PyTorch-Lighting for training, which enables quick fine-tuning of GeoFMs based on a config yaml file.
You find the documentation here: https://ibm.github.io/terratorch/quick_start/.

Make sure to prepare your dataset according to [DATASET_PREPARATION.md](DATASET_PREPARATION.md).

Activate your venv
```shell
source venv/bin/activate
```

## Fine-tuning via CLI

You need to customise a fine-tuning config for your dataset. You can start with on of the examples and adapt it to your data. 
We explain the details in the workshop.

You start a TerraTorch training with: 
```shell
terratorch fit --config configs/forestnet_vit.yaml
```


### Classification

Config example: [forestnet_vit.yaml](configs%2Fforestnet_vit.yaml)

### Segmentation

### Pixelwise Regression

## Training via Python

Please see this [Tutorial](https://github.com/IBM/terratorch/blob/main/examples/notebooks/Tutorial.ipynb) for example code in how to use TerraTorch within python.