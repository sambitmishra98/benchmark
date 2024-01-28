#!/bin/bash
#SBATCH --job-name="venv-build"
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-06:00:00
#SBATCH --mem=80G
#SBATCH --output=PyFR-build-PVC.out
#SBATCH --no-requeue
#SBATCH --partition=pvc
#SBATCH --ntasks=24
#SBATCH --gres=gpu:pvc:4
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

    setup_base
    export_all_versions

    add_installation_to_path gcc      $BUILD_GCC_VER     $PKG_LOCAL

    add_installation_to_path ${BUILD_NAME_PYTHON}-${BUILD_TAG_PYTHON}/libffi  $BUILD_LIBFFI_VER  $PKG_LOCAL
    add_installation_to_path ${BUILD_NAME_PYTHON}-${BUILD_TAG_PYTHON}/openssl $BUILD_OPENSSL_VER $PKG_LOCAL
    add_installation_to_path ${BUILD_NAME_PYTHON}-${BUILD_TAG_PYTHON}/python  $BUILD_PYTHON_VER  $PKG_LOCAL

    add_installation_to_path ${BUILD_NAME_MPI}-${BUILD_TAG_MPI}/mpich     $BUILD_MPICH_VER $PKG_LOCAL

    add_optional_pyfr_dependencies

    source $VENV_LOCAL/venv-${BUILD_NAME_VENV}-${BUILD_TAG_VENV}/bin/activate
# ------------------------------------------------------------------------------
# Setup PyFR
# ------------------------------------------------------------------------------

    CMD="${BUILD_PATH}/pyfr.build ${BUILD_NAME_VENV} ${BUILD_TAG_VENV} ${np}"
    echo -e "\n$CMD\n"
    eval $CMD

echo -e "\nPyFR setup complete\n"
