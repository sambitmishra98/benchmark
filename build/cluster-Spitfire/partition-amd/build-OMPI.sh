# First, ensure that UCX was installed 

if [ ! -d $INSTALLS/ucx/$UCX_SHA ]; then
    echo -e "UCX $UCX_SHA does not exist at $INSTALLS/ucx/$UCX_SHA\n"
    exit 1
fi

# If we already have github repo cloned, we can skip the git clone step
if [ ! -d $DOWNLOADS/ompi/$OMPI_SHA ]; then
    git clone --recursive https://github.com/open-mpi/ompi.git $DOWNLOADS/ompi/$OMPI_SHA
    echo -e "Cloned OpenMPI from https://github.com/open-mpi/ompi.git since it did not already exist\n"
else
    echo -e "OpenMPI already exists at $DOWNLOADS/ompi/$OMPI_SHA\n"
fi

cd $DOWNLOADS/ompi/$OMPI_SHA

# If we have already build this version of OpenMPI, we can skip the build step and move on to testing it

if [ -d $INSTALLS/ompi/$OMPI_SHA ]; then
    echo -e "OpenMPI $OMPI_SHA already exists at $INSTALLS/ompi/$OMPI_SHA\n"
    add_installation_to_path ompi "$OMPI_SHA" "$INSTALLS"
    ompi_info -a

    echo -e "Delete this to re-install"
    mpiexec -n 12 hostname    
    exit 0
fi

CURRENT_OMPI_SHA=$(git rev-parse HEAD)

if [ "$CURRENT_OMPI_SHA" = "$OMPI_SHA" ]; then
    echo -e "OpenMPI is already at the correct SHA. \n"
else
    echo -e "OpenMPI is not at the correct SHA\n"
    git checkout $OMPI_SHA
fi

./autogen.pl

# Sphinx is required to build OpenMPI. Check for the venv

if [ ! -d ompi-docs-venv ]; then
    echo -e "Creating a virtual environment for Sphinx\n"
    python3 -m venv ompi-docs-venv
    source ompi-docs-venv/bin/activate
    pip3 install -r docs/requirements.txt
else
    echo -e "Sphinx virtual environment already exists\n"
    source ompi-docs-venv/bin/activate
fi


if [ -d $INSTALLS/ompi/$OMPI_SHA ]; then
    echo -e "OpenMPI $OMPI_SHA already exists at $INSTALLS/ompi/$OMPI_SHA\n"
    add_installation_to_path ompi "$OMPI_SHA" "$INSTALLS"
    ompi_info -a

    # Test for hostname
    mpiexec -n 6 hostname    

    echo -e "Delete this to re-install"

    exit 0
fi

CMD="./configure --prefix=$INSTALLS/ompi/$OMPI_SHA --enable-shared "
CMD+=" --with-ucx=$INSTALLS/ucx/$UCX_SHA "
CMD+=" --with-rocm=/opt/rocm-6.1.1 "
CMD+=" --without-ofi --without-libfabric --without-verbs " # NEVER CHANGE THIS
CMD+=" --enable-mca-dso "

echo $CMD
eval $CMD
make -j 6 ; make install

#add_installation_to_path ucx "$UCX_SHA" "$INSTALLS"
add_installation_to_path ompi "$OMPI_SHA" "$INSTALLS"

# Test the installation

echo -e "Test 1: ompi_info"
ompi_info -a

echo -e "Test 2: hostname"
mpiexec -n 6 hostname    

# - - - - -