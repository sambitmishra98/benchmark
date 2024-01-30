#!/bin/bash
#SBATCH --job-name="mpi-build"
#SBATCH --nodes=2
#SBATCH --reservation=benchmarking
#SBATCH --exclusive
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-06:00:00
#SBATCH --mem=80G
#SBATCH --output=MPI-build-A100.out
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

CMD="${BUILD_PATH}/build_scripts/build_mpi.script"
echo -e "\n$CMD\n"
eval $CMD

# ------------------------------------------------------------------------------
# CHECK IF BUILD WAS SUCCESSFUL
# ------------------------------------------------------------------------------

#add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/mpich   ${BUILD_MPICH_VER}   ${PKG_LOCAL}
add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/ucx     ${BUILD_UCX_VER}     ${PKG_LOCAL}
add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/openmpi ${BUILD_OPENMPI_VER} ${PKG_LOCAL}

# ------------------------------------------------------------------------------
# RUN OSU MICROBENCHMARKS
# ------------------------------------------------------------------------------
echo -e "\nRunning OSU microbenchmarks\n"
echo -e "\n=================================================================\n"
echo -e "\n OSU Bandwidth\n"
srun -N2 --tasks-per-node=1 -n 2 $GIT_LOCAL/${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/osu-micro-benchmarks/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw
# echo -e "\n-----------------------------------------------------------------\n"
# echo -e "\n OSU Bi-Directional Bandwidth\n"
# mpirun -np 2 $GIT_LOCAL/${BUILD_NAME}-${BUILD_TAG}/osu-micro-benchmarks/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bibw
# echo -e "\n-----------------------------------------------------------------\n"
