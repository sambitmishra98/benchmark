#!/bin/bash
#SBATCH --job-name="ompi-script"
#SBATCH --nodes=1
##SBATCH --exclusive
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-06:00:00
#SBATCH --mem=80G
#SBATCH --output=python3-build-hip.out
#SBATCH --no-requeue
#SBATCH --partition=amd
#SBATCH --ntasks=3
#SBATCH --gres=gpu:3
#SBATCH --cpus-per-gpu=8

# ------------------------------------------------------------------------------
# Check environment
# ------------------------------------------------------------------------------

. /etc/profile.d/modules.sh
module purge

rocm-smi

source ~/.bashrc
echo -e "\n================================================================="

export BUILD_NAME="build3"
export BUILD_TAG="ac038"
export BUILD_PATH="/mnt/share/sambit98/EFFORT_BENCHMARK/benchmark/build"

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

setup_base
export_all_versions
add_installation_to_path gcc      $BUILD_GCC_VER     $PKG_LOCAL

# ------------------------------------------------------------------------------
# Build
# ------------------------------------------------------------------------------

CMD="${BUILD_PATH}/python.build ${BUILD_NAME} ${BUILD_TAG} ${BUILD_LIBFFI_VER} ${BUILD_OPENSSL_VER} ${BUILD_PYTHON_VER}"
echo -e "\n$CMD\n"
eval $CMD

add_installation_to_path ${BUILD_NAME}-${BUILD_TAG}/libffi  ${BUILD_LIBFFI_VER}  $PKG_LOCAL
add_installation_to_path ${BUILD_NAME}-${BUILD_TAG}/openssl ${BUILD_OPENSSL_VER} $PKG_LOCAL
add_installation_to_path ${BUILD_NAME}-${BUILD_TAG}/python  ${BUILD_PYTHON_VER}  $PKG_LOCAL

which python3

echo -e "\nSimulation ends\n"
