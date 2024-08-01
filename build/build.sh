# - - - - - 
# INTRO
# - - - - -


# ----------------------------------------------

# Set and check all variables below

export   SCRATCH=/mnt/share/sambit98
export DOWNLOADS="${SCRATCH}/.downloads"
export  INSTALLS="${SCRATCH}/.local-spitfire"


# UCX version to build
UCX_SHA=5f5b5c18bb11d0bba323b97a8cc9a2a5b7c060db
OMPI_SHA=439b23db6288f0370f6fcc80c8c0a06ad86d6873

if [  ${#UCX_SHA} -ne 40 ]; then echo "Invalid  UCX_SHA" ; exit 1 ; fi
if [ ${#OMPI_SHA} -ne 40 ]; then echo "Invalid OMPI_SHA" ; exit 1 ; fi

# ----------------------------------------------






add_installation_to_path() {
    local name=$1
    local version=$2
    local install_root=$3
    local install_dir="${install_root}/${name}/${version}"

    # if the base directory does not exist, then echo a warning and return
    if [ ! -d "${install_dir}" ]; then
        echo -e "\e[31mERROR IN PATH ADDITION: ${install_dir} DOES NOT EXIST !!!!\e[0m"; return
    else
        echo -e "\e[32mAdding ${name} installation at ${install_dir} to PATH\e[0m"

        [ -d "${install_dir}/bin"           ] && export            PATH="${install_dir}/bin:$PATH"
        [ -d "${install_dir}/include"       ] && export           CPATH="${install_dir}/include:$CPATH"
        [ -d "${install_dir}/include"       ] && export          CPPATH="${install_dir}/include:$CPPATH"
        [ -d "${install_dir}/lib"           ] && export          LDPATH="${install_dir}/lib:$LDPATH"
        [ -d "${install_dir}/lib64"         ] && export          LDPATH="${install_dir}/lib64:$LDPATH"
        [ -d "${install_dir}/lib"           ] && export    LIBRARY_PATH="${install_dir}/lib:$LIBRARY_PATH"
        [ -d "${install_dir}/lib64"         ] && export    LIBRARY_PATH="${install_dir}/lib64:$LIBRARY_PATH"
        [ -d "${install_dir}/lib"           ] && export LD_LIBRARY_PATH="${install_dir}/lib:$LD_LIBRARY_PATH"
        [ -d "${install_dir}/lib64"         ] && export LD_LIBRARY_PATH="${install_dir}/lib64:$LD_LIBRARY_PATH"
        [ -d "${install_dir}/lib/pkgconfig" ] && export PKG_CONFIG_PATH="${install_dir}/lib/pkgconfig:$PKG_CONFIG_PATH"
    fi }

add_installation_to_path "rocm-6.1.1" ""             "/opt/"
add_installation_to_path  gcc         $BUILD_GCC_VER $PKG_LOCAL


# If does not exist, get it
if [ ! -d $INSTALLS/ucx/$UCX_SHA ]; then
    git clone https://github.com/openucx/ucx.git $INSTALLS/ucx/$UCX_SHA
fi

echo "Building UCX SHA: $UCX_SHA"
cd $INSTALLS/ucx/$UCX_SHA
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
CMD+=" --disable-logging "
CMD+=" --disable-debug "
CMD+=" --disable-assertions "
CMD+=" --disable-params-check "

echo $CMD
eval $CMD

make -j 24 ; make install

add_installation_to_path ucx "$UCX_SHA" ${INSTALL_MPI}
