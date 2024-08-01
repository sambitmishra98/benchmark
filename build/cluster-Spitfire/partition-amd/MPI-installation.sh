# - - - - - 
# INTRO
# - - - - -


# ----------------------------------------------

# Set and check all variables below


# Locations to build into
export   SCRATCH=/mnt/share/sambit98
export DOWNLOADS="${SCRATCH}/.downloads"
export  INSTALLS="${SCRATCH}/.local-spitfire"

# Git SHA versions to build
export  UCX_SHA=5f5b5c18bb11d0bba323b97a8cc9a2a5b7c060db
export OMPI_SHA=439b23db6288f0370f6fcc80c8c0a06ad86d6873  # 4.1.6 WORKED
#export OMPI_SHA=b4390af9ad3bd0384572fccdd7e410e7614df1f8  # 5.0.5 Bus error
#export OMPI_SHA=6db5e83b737a9b70c4e77a2bcf06ab641adffe2a  # 5.0.2 Bus error
#export OMPI_SHA=79f675e98ca842c7feb7615b292a202e3c0646ee  # 5.0.1 Bus error
#export  OMPI_SHA=d0fe8ef8113906ac485c8d4a2e687d6bdcaa8305 # 5.0.0 Bus error

if [  ${#UCX_SHA} -ne 40 ]; then echo "Invalid  UCX_SHA" ; exit 1 ; fi
if [ ${#OMPI_SHA} -ne 40 ]; then echo "Invalid OMPI_SHA" ; exit 1 ; fi

# ----------------------------------------------
# Call all sbatch scripts for setup

sbatch clusterbuild-UCX.spitfire_amd
sbatch clusterbuild-OMPI.spitfire_amd

