
## Specifications

CPU: AMD EPYC 7282 16-Core Processor
GPU: AMD MI100

$ ibstat
CA 'mlx5_0'
        CA type: MT4123
        Number of ports: 1
        Firmware version: 20.39.1002
        Hardware version: 0
        Node GUID: 0xb8cef603008bbf1c
        System image GUID: 0xb8cef603008bbf1c
        Port 1:
                State: Active
                Physical state: LinkUp
                Rate: 100
                Base lid: 29
                LMC: 0
                SM lid: 2
                Capability mask: 0xa659e84a
                Port GUID: 0xb8cef603008bbf1c
                Link layer: InfiniBand

## Setup scripts

main script - Calls all the other scripts we need in this setup
        $HASHES for all installations

        UCX SBATCH script - Environment setup for installing UCX in a unique location
        Unique identification by the hash of the script and configuration flags used
        If already available, then exit 
                UCX script - Installs UCX

        OMPI SBATCH script - Environment setup for installing OpenMPI in a unique location
        Unique identification by the hash of the script and configuration flags used
        If already available, then exit 
                OMPI script - Installs OpenMPI
