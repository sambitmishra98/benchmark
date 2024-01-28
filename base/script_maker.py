import os
import numpy as np

class ScriptMaker:
    def __init__(self, prefix = ''):

        self.simulation_wait_time = '24' # in hours

    def generate_slurm_script(self, prefix, nodelist, steps, backend, caware, order, precision, nodes, ntasks , etype, elems, partition, gpu):

        # If the string nodelist contains the substring 'ac' then we are working on the ACES cluster
        # else if nodelist contains the substring 'fc' then we are working on the FASTER cluster
        if   'ac'          in nodelist: cluster = 'ACES'
        elif 'fc'          in nodelist: cluster = 'FASTER'
        elif 'g'           in nodelist: cluster = 'Grace'
        elif 'spitfire-ng' in nodelist: cluster = 'Spitfire'
        else:                  raise ValueError(f"Cluster not supported")

        mpi_lib = 'mpich'   # Use MPICH everywhere
        #export MPIR_CVAR_ENABLE_GPU=1 ; 
        if   backend ==   'cuda': ompi_mca = f'--mca accelerator cuda' #
        elif backend ==    'hip': ompi_mca = f'--mca accelerator rocm' #
        elif backend == 'opencl': ompi_mca = f'--mca accelerator null' #
        elif backend == 'openmp': ompi_mca = f'--mca accelerator null' #
        elif backend in ['metal']: 
            raise ValueError(f"Backend {backend} yet to be supported")
        else: 
            raise ValueError(f"Backend {backend} DOES NOT EXIST!!")

        if gpu == 'pvc':
            prerun='xpumcli dump -d -1 -m 0,2,3,5,6,7,17,18 -i 10 > "log_gpus" &\n' \
                     'xpumanager_pid=$!\n'  
            postrun='kill $xpumanager_pid'
        else:
            prerun=''
            postrun=''

        if 'spitfire-ng' in nodelist:
            GPUS=f'#SBATCH --gres=gpu:{int(np.ceil(ntasks/nodes))}'
        else:
            GPUS=f'#SBATCH --gres=gpu:{gpu}:{int(np.ceil(ntasks/nodes))}'

        if   partition == 'pvc' and gpu ==   'pvc': pass
        elif partition == 'gpu' and gpu ==  'h100': pass
        elif partition == 'gpu' and gpu ==  'a100': pass
        elif partition == 'gpu' and gpu ==   'a40': pass
        elif partition == 'gpu' and gpu ==   'a10': pass
        elif partition == 'gpu' and gpu ==    't4': pass
        elif partition == 'all' and gpu ==  'v100': pass
        elif partition == 'amd' and gpu == 'mi100': pass
        else: raise ValueError(f"Partition {partition} not supported")

        job_name = f"{prefix}partition{partition}_nodelist{nodelist}_" \
                   f"steps{steps}_backend{backend}_caware{caware}_order{order}_precision{precision}_nodes{nodes}_" \
                   f"tasks{ntasks}_{etype}{elems}"

        return f'''#!/bin/bash
#SBATCH --job-name="{job_name}"
#SBATCH --nodes={nodes}
##SBATCH --exclusive
##SBATCH --reservation=r3_debugging
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-{self.simulation_wait_time}:00:00
#SBATCH --mem=100G
#SBATCH --output={job_name}.out
#SBATCH --no-requeue
#SBATCH --partition={partition}
#SBATCH --ntasks={ntasks}
{GPUS}
#SBATCH --cpus-per-gpu=2
##SBATCH --nodelist={nodelist}

source ~/.bashrc

CMD="/sw/local/bin/query_gpu.sh ; nvidia-smi"; echo -e "\\nExecuting command:\\n==================\\n$CMD\\n";
eval $CMD;

CMD="clinfo -l"; echo -e "\\nExecuting command:\\n==================\\n$CMD\\n"; 
eval $CMD;

numnodes=$SLURM_JOB_NUM_NODES
mpi_tasks_per_node=$(echo "$SLURM_TASKS_PER_NODE" | sed -e  's/^\\([0-9][0-9]*\\).*$/\\1/')
np=$[${{SLURM_JOB_NUM_NODES}}*${{mpi_tasks_per_node}}]

echo "Running on master node: `hostname`"
echo "Time: `date`"
echo "Current directory: `pwd`"
echo -e "JobID: $SLURM_JOB_ID\\n======"
echo -e "Tasks=${{SLURM_NTASKS}},nodes=${{SLURM_JOB_NUM_NODES}}, mpi_tasks_per_node=${{mpi_tasks_per_node}} (OMP_NUM_THREADS=$OMP_NUM_THREADS)"

# ------------------------------------------------------------------------------
inif="../../configs/steps{steps}_caware{caware}_order{order}_precision{precision}_tasks{ntasks}_{etype}{elems}.ini"
meshf="../../partitions/tasks{ntasks}_{etype}{elems}.pyfrm"; 
# ------------------------------------------------------------------------------

echo $PATH | tr ':' '\\n'
echo "PYFR_XSMM_LIBRARY_PATH=$PYFR_XSMM_LIBRARY_PATH"
echo "PYFR_METIS_LIBRARY_PATH=$PYFR_METIS_LIBRARY_PATH"
echo "PYFR_CLBLAST_LIBRARY_PATH=$PYFR_CLBLAST_LIBRARY_PATH"

# Run subscript
    CMD="time mpirun {ompi_mca} -n {ntasks} pyfr run -b {backend} $meshf $inif"
    echo -e "\\nExecuting command:\\n==================\\n$CMD\\n";
    eval $CMD;

# ------------------------------------------------------------------------------

echo -e "\\nSimulation ends\\n"
        '''

    def write_script_to_file(self, script, output):
        try:
            with open(output, 'w') as f:
                f.write(script)
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False

        return True

    def make_scripts(self, nprefix, 
                           npartition, nnodelist,  ngpu,
                           nsteps, nbackend, ncaware, norder, nprecision,
                           nnodes, ntasks_per_node, 
                           netype, nelements,):

        os.system("mkdir -p scripts")
        
        for prefix, nodelist, steps, backend, caware, order, precision, nodes, tasks_per_node, etype, elements, partition, gpu in zip(nprefix,nnodelist, nsteps, nbackend, ncaware, norder, nprecision, nnodes, ntasks_per_node, netype, nelements, npartition, ngpu):

            tasks = nodes * tasks_per_node

            script = self.generate_slurm_script(prefix, nodelist, steps, backend, caware, order, precision, nodes, tasks, etype, elements, partition, gpu)
            output = f"scripts/{prefix}partition{partition}_gpu{gpu}_nodelist{nodelist}_steps{steps}_backend{backend}_caware{caware}_order{order}_precision{precision}_nodes{nodes}_tasks{tasks}_{etype}{elements}.sh"
            if not os.path.isfile(output):
                self.write_script_to_file(script, output)
                print(f"Script created: {output}")
            else:
                print(f"Script  exists: {output}")
