# First, ensure that UCX and OpenMPI are in place

if [ ! -d $INSTALLS/ucx/$UCX_SHA ]; then
    echo -e "UCX $UCX_SHA does not exist at $INSTALLS/ucx/$UCX_SHA\n"
    exit 1
else 
    echo -e "UCX $UCX_SHA exists at $INSTALLS/ucx/$UCX_SHA\n"
    ucx_info -v
fi

if [ ! -d $INSTALLS/ompi/$OMPI_SHA ]; then
    echo -e "OpenMPI $OMPI_SHA does not exist at $INSTALLS/ompi/$OMPI_SHA\n"
    exit 1
else
    echo -e "OpenMPI $OMPI_SHA exists at $INSTALLS/ompi/$OMPI_SHA\n"
    ompi_info -a
fi

# OSU-Micro-Benchmarks do not have a github repo.
cd $DOWNLOADS/osu-mb




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