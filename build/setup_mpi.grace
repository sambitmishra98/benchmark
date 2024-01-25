#!/bin/bash
#SBATCH --job-name="mpi-build"
#SBATCH --nodes=1
##SBATCH --exclusive
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-06:00:00
#SBATCH --mem=80G
#SBATCH --output=MPI-build-cuda.out
#SBATCH --no-requeue
#SBATCH --partition=gpu
#SBATCH --ntasks=24
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-gpu=24

# ------------------------------------------------------------------------------
# Check environment
# ------------------------------------------------------------------------------


/sw/local/bin/query_gpu.sh

nvidia-smi -L ; clinfo -l
source ~/.bashrc
echo -e "\n================================================================="

export BUILD_NAME="cuda"
export BUILD_TAG="grace1"
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
#    add_installation_to_path rocm-6.0.0 ""             "/opt"
    add_installation_to_path  cuda-12.2  ""             "/usr/local/"
    add_installation_to_path  gcc        $BUILD_GCC_VER $PKG_LOCAL

# ------------------------------------------------------------------------------
# Build
# ------------------------------------------------------------------------------

CMD="${BUILD_PATH}/openmpi.build ${BUILD_NAME} ${BUILD_TAG} ${BUILD_UCX_VER} ${BUILD_OPENMPI_VER}"
echo -e "\n$CMD\n"
eval $CMD

add_installation_to_path ${BUILD_NAME}-${BUILD_TAG}/ucx     ${BUILD_UCX_VER}     $PKG_LOCAL
add_installation_to_path ${BUILD_NAME}-${BUILD_TAG}/openmpi ${BUILD_OPENMPI_VER} $PKG_LOCAL

which mpirun
ompi_info

# ------------------------------------------------------------------------------
# Test build with osu_microbenchmarks and other CUDA benchmarks
# ------------------------------------------------------------------------------

# CMD="${BUILD_PATH}/osu_microbenchmarks.build ${BUILD_NAME} ${BUILD_TAG} ${BUILD_OPENMPI_VER}"
# echo -e "\n$CMD\n"
# eval $CMD

# ------------------------------------------------------------------------------
# RUN OSU MICROBENCHMARKS
# ------------------------------------------------------------------------------
# echo -e "\nRunning OSU microbenchmarks\n"
# echo -e "\n=================================================================\n"
# echo -e "\n OSU Bandwidth\n"
# mpirun -np 2 $GIT_LOCAL/${BUILD_NAME}-${BUILD_TAG}/osu-micro-benchmarks/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw
# echo -e "\n-----------------------------------------------------------------\n"
# echo -e "\n OSU Bi-Directional Bandwidth\n"
# mpirun -np 2 $GIT_LOCAL/${BUILD_NAME}-${BUILD_TAG}/osu-micro-benchmarks/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bibw
# echo -e "\n-----------------------------------------------------------------\n"