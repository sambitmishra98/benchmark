#!/bin/bash
#SBATCH --job-name="Python-build"
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-06:00:00
#SBATCH --mem=80G
#SBATCH --output=Python-build-A100.out
#SBATCH --no-requeue
#SBATCH --partition=gpu
#SBATCH --ntasks=24
#SBATCH --gres=gpu:a100:2
#SBATCH --cpus-per-gpu=12


# ------------------------------------------------------------------------------
# Check environment
# ------------------------------------------------------------------------------

source ~/.bashrc
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

        BUILD_A100_2024_01_28_ENV
        add_installation_to_path  gcc        $BUILD_GCC_VER $PKG_LOCAL

# ------------------------------------------------------------------------------
# Build
# ------------------------------------------------------------------------------

CMD="${BUILD_PATH}/build_scripts/build_python.script"
echo -e "\n$CMD\n"
eval $CMD

add_installation_to_path ${BUILD_NAME_PYTHON}-${BUILD_TAG_PYTHON}/libffi  ${BUILD_LIBFFI_VER} ${PKG_LOCAL}
add_installation_to_path ${BUILD_NAME_PYTHON}-${BUILD_TAG_PYTHON}/openssl ${BUILD_OPENSSL_VER} ${PKG_LOCAL}
add_installation_to_path ${BUILD_NAME_PYTHON}-${BUILD_TAG_PYTHON}/python  ${BUILD_PYTHON_VER} ${PKG_LOCAL}

echo -e "\nSimulation ends\n"
