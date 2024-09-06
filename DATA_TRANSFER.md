# Data transfer

You need to transfer your data to the `judac` storage system in Julich to train a model with your data. 

Please note that we have storage limits on the system. We kindly ask everyone to not transfer more than 500GB of data and not more than 100k files. 
If you have more files, please subsample your dataset before the transfer or convert to a different file format (requires custom TerraTorch dataset class).

Follow these steps:
1. You have prepared your data locally (or on your server).
2. You have created an account for project `training2413` and got access to judoor from JSC (Project page: https://judoor.fz-juelich.de/projects/training2431/).
3. Add your ssh key and ip address for the `judac` system (Log in to https://judoor.fz-juelich.de -> Systems -> `judac` -> `Manage SSH-keys`). 
The website displays the ip address of your local machine. If you transfer the data from a server use a cli tool like `curl ipinfo.io/ip` to get the servers' ip address.
To check if everything is working, you can ssh into `judac` with:
```shell
# Make sure the ssh key and ip are matching.
ssh <user_name>@judac.fz-juelich.de
# Project data directory
cd /p/scratch/training2431/
# Please create a user directory for yourself
mkdir <user_dir>
```

4. Transfer your data to the `judac` system with:

```shell
rsync -av --progress <local/path/to/your/dataset> <user_name>@judac.fz-juelich.de:/p/scratch/training2431/<user_dir>/
# If you get a ` Permission denied (publickey)` error, please check your IP address as it can change (https://judoor.fz-juelich.de/account/a/JSC_LDAP/blumenstiel1/system/judac/add_ssh_key)

# If your ssh key is not found correctly, use:
rsync -av -e 'ssh -i <path/to/ssh>/.ssh/id_ed25519 -o StrictHostKeychecking=no' --progress <local/path/to/your/dataset> <user_name>@judac.fz-juelich.de:/p/scratch/training2431/<user_dir>/

# Example for ForestNet
rsync -av --progress data/ForestNetDataset blumenstiel1@judac.fz-juelich.de:/p/scratch/training2431/benediktblumenstiel/

```

Please respect the storage limits of 500GB of data and 100k files per person.