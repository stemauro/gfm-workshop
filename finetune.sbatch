#!/usr/bin/env bash

#SBATCH --account=training2431
#SBATCH --partition=dc-gpu-devel
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=8
# Use only physical cores. (Can use up to 2 threads per core.)
#SBATCH --threads-per-core=1
#SBATCH --time=00:15:00


#--gres=gpu:4
# --reservation=training2431

#SBATCH --output="slurm-%j.out"
#SBATCH --error="slurm-%j.err"

curr_file="$(scontrol show job "$SLURM_JOB_ID" | grep '^[[:space:]]*Command=' | head -n 1 | cut -d '=' -f 2-)"
curr_dir="$(dirname "$curr_file")"

# Propagate the specified number of CPUs per task to each `srun`.
export SRUN_CPUS_PER_TASK="$SLURM_CPUS_PER_TASK"

source "$curr_dir"/activate.sh

export MASTER_ADDR="$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)"
if [ "$SYSTEMNAME" = juwelsbooster ] \
       || [ "$SYSTEMNAME" = juwels ] \
       || [ "$SYSTEMNAME" = jurecadc ] \
       || [ "$SYSTEMNAME" = jusuf ]; then
    # Allow communication over InfiniBand cells on JSC machines.
    MASTER_ADDR="$MASTER_ADDR"i
fi
export MASTER_PORT=54123

# Prevent NCCL not figuring out how to initialize.
export NCCL_SOCKET_IFNAME=ib0
# Prevent GLOO not being able to communicate.
export GLOO_SOCKET_IFNAME=ib0

#srun env -u CUDA_VISIBLE_DEVICES python -u -m torchrun_jsc \
#       --nproc_per_node=gpu \
#       --nnodes="$SLURM_JOB_NUM_NODES" \
#       --rdzv_id="$SLURM_JOB_ID" \
#       --rdzv_endpoint="$MASTER_ADDR":"$MASTER_PORT" \
#       --rdzv_backend=c10d \
#       "$curr_dir"/main.py "$@"

srun env -u CUDA_VISIBLE_DEVICES python -m terratorch fit "$@"
