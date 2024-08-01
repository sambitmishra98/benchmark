# If we already have github repo cloned, we can skip the git clone step
if [ ! -d $DOWNLOADS/ucx/$UCX_SHA ]; then
    git clone https://github.com/openucx/ucx.git $DOWNLOADS/ucx/$UCX_SHA
    echo -e "Cloned UCX from https://github.com/openucx/ucx.git since it did not already exist\n"
else
    echo -e "UCX already exists at $DOWNLOADS/ucx/$UCX_SHA\n"
fi

cd $DOWNLOADS/ucx/$UCX_SHA



# If we have already build this version of UCX, we can skip the build step and move on to testing it

if [ -d $INSTALLS/ucx/$UCX_SHA ]; then
    echo -e "UCX $UCX_SHA already exists at $INSTALLS/ucx/$UCX_SHA\n"
    add_installation_to_path ucx "$UCX_SHA" "$INSTALLS"
    ucx_info -d

    echo -e "Delete this to re-install"

    exit 0
fi

git checkout $UCX_SHA
./autogen.sh
CMD="./configure --prefix=$INSTALLS/ucx/$UCX_SHA --enable-shared "
CMD+=" --enable-devel-headers "
CMD+=" --enable-mt "
CMD+=" --enable-cma "
CMD+=" --enable-optimizations "
CMD+=" --with-rc "
CMD+=" --with-dc "
CMD+=" --with-ib-hw-tm "
CMD+=" --with-rocm=/opt/rocm-6.1.1 "
echo $CMD
eval $CMD
make -j 24 ; make install

add_installation_to_path ucx "$UCX_SHA" "$INSTALLS"

# Test the installation
ucx_info -d



# ------------------------------------------------------------------------------
# REPEAT FOR OPENMPI
# ------------------------------------------------------------------------------

# If we already have github repo cloned, we can skip the git clone step
if [ ! -d $DOWNLOADS/ompi/$OMPI_SHA ]; then
    git clone https://github.com/open-mpi/ompi.git $DOWNLOADS/ompi/$OMPI_SHA
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

    exit 0
fi

git checkout $OMPI_SHA
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

CMD="./configure --prefix=$INSTALLS/ompi/$OMPI_SHA --enable-shared "
CMD+=" --with-ucx=$INSTALLS/ucx/$UCX_SHA "
CMD+=" --with-rocm=/opt/rocm-6.1.1 "

echo $CMD
eval $CMD
make -j 6 ; make install

add_installation_to_path ompi "$OMPI_SHA" "$INSTALLS"

# Test the installation

ompi_info -a

# - - - - -