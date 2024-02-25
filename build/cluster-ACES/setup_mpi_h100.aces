#!/bin/bash
#SBATCH --job-name="mpi-build"
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --reservation=nsight
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-06:00:00
#SBATCH --mem=80G
#SBATCH --output=MPI-build-H100.out
#SBATCH --no-requeue
#SBATCH --partition=gpu
#SBATCH --ntasks=16
#SBATCH --gres=gpu:h100:2
#SBATCH --cpus-per-gpu=8
#SBATCH --nodelist=ac055

# ------------------------------------------------------------------------------
# Check environment
# ------------------------------------------------------------------------------

/sw/local/bin/query_gpu.sh

nvidia-smi -L ; clinfo -l
source ~/.bashrc
echo -e "\n================================================================="

# ------------------------------------------------------------------------------
# Print SLURM settings
# ------------------------------------------------------------------------------

numnodes=$SLURM_JOB_NUM_NODES
mpi_tasks_per_node=$(echo "$SLURM_TASKS_PER_NODE" | sed -e  's/^\([0-9][0-9]*\).*$/\1/')
np=$[${SLURM_JOB_NUM_NODES}*${mpi_tasks_per_node}]

echo "Running on master node: `hostname`"
echo "Time: `date`"
echo "Current directory: `pwd`"
echo -e "JobID: $SLURM_JOB_ID\n================================================================="
echo -e "Tasks=${SLURM_NTASKS},\
         nodes=${SLURM_JOB_NUM_NODES}, \
         mpi_tasks_per_node=${mpi_tasks_per_node} \
         (OMP_NUM_THREADS=$OMP_NUM_THREADS)"

# ------------------------------------------------------------------------------
# Setup paths
# ------------------------------------------------------------------------------

LATEST_BUILD_H100
ml CUDA/$BUILD_EASY_CUDA_VER
add_installation_to_path gcc      $BUILD_GCC_VER     $PKG_LOCAL

# ------------------------------------------------------------------------------
# Build
# ------------------------------------------------------------------------------

CMD="${BUILD_PATH}/build_scripts/build_mpi.script"
echo -e "\n$CMD\n"
eval $CMD

add_installation_to_path final-compute-amd/ucx     $BUILD_UCX_VER     $PKG_LOCAL
add_installation_to_path final-compute-amd/openmpi $BUILD_OPENMPI_VER $PKG_LOCAL

# ------------------------------------------------------------------------------
# CHECK IF BUILD WAS SUCCESSFUL
# ------------------------------------------------------------------------------

#add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/mpich   ${BUILD_MPICH_VER}   ${PKG_LOCAL}
add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/ucx     ${BUILD_UCX_VER}     ${PKG_LOCAL}
add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/openmpi ${BUILD_OPENMPI_VER} ${PKG_LOCAL}
