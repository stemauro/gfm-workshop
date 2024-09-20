# TerraTorch

TerraTorch is a fine-tuning toolkit for Geospatial Foundation Models (GeoFMs). 
It uses PyTorch-Lighting for training, which enables quick fine-tuning of GeoFMs based on a config yaml file.
You find the documentation here: https://ibm.github.io/terratorch/quick_start/.

Make sure to prepare your dataset according to [DATASET_PREPARATION.md](DATASET_PREPARATION.md).

## Local setup

Activate your venv
```shell
source venv/bin/activate
```

If you have not created one already, create a venv and install terratorch
```shell
python -m venv venv
source venv/bin/activate
pip install terratorch 

# For Tutorials install:
# pip install jupyter tensorboard wandb matplotlib 
```

If you want to train with NVIDIA GPUS, please check that a PyTorch version with GPU support (CUDA) is installed.

```yaml
pip list | grep "cuda"
```

If CUDA is not available, reinstall torch with cuda following https://pytorch.org.
E.g. you could use this command for CUDA 11.8 support:
```yaml
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

You might want to start with a fresh venv: First, install torch with cuda support and afterward terratorch for the remaining packages.

You can check if torch finds a GPU with: 
```yaml
python -c "import torch; print(torch.cuda.is_available())"
```


## Fine-tuning via CLI

You need to customise a fine-tuning config for your dataset. You can start with on of the examples and adapt it to your data. 
We explain the details in the workshop.

You start a TerraTorch training with: 
```shell
terratorch fit --config configs/<your_config>.yaml
```

### Classification

Config example: [forestnet_vit.yaml](configs%2Fforestnet_vit.yaml)

Run training with 
```shell
terratorch fit --config configs/forestnet_vit.yaml
```

Config example with Timm classification models: [forestnet_timm.yaml](configs%2Fforestnet_timm.yaml)

Config example with torchgeo dataset: [eurosat.yaml](https://github.com/IBM/terratorch/blob/main/examples/confs/eurosat.yaml)

### Segmentation

Config example: [burnscars_vit.yaml](configs%2Fburnscars_vit.yaml)

Run training with 
```shell
terratorch fit --config configs/burnscars_vit.yaml
```

Config example with Segmentation Models PyTorch: [burnscars_smp.yaml](configs%2Fburnscars_smp.yaml)

Config example with dataset Sen1Floods11: [sen1floods11_vit.yaml](https://github.com/IBM/terratorch/blob/main/examples/confs/sen1floods11_vit.yaml)

### Pixelwise Regression

Config example: [granite_biomass.yaml](https://github.com/ibm-granite/granite-geospatial-biomass/blob/main/configs/config.yaml)

### Tensorboard

Follow the training via tensorboard. The logs are saved to `default_root_dir` in your yaml config. 
You might need to install it with `pip install tensorboard`. 

```shell
# ForestNet logs
tensorboard --logdir output --host $(hostname -f) --port 9010
```

## Training via Python

Check the tutorials to understand how to use TerraTorch in Python code. 
The tutorials initialize step by step the different components of PyTorch Lightning which is used by TerraTorch.

Tutorial with Prithvi:  [Tutorial_prithvi.ipynb](Tutorial_prithvi.ipynb)

Tutorial with Segmentation Models PyTorch: [Tutorial_segmentation_smp.ipynb](Tutorial_segmentation_smp.ipynb)

Tutorial with Timm for classification tasks: [Tutorial_classification_timm.ipynb](Tutorial_classification_timm.ipynb)

Example notebook for biomass estimation: https://github.com/ibm-granite/granite-geospatial-biomass/blob/main/notebooks/agb_getting_started.ipynb
