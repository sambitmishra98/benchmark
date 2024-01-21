import os
import numpy as np

class ScriptMaker:
    def __init__(self, prefix = ''):

        self.prefix = prefix
        self.simulation_wait_time = '6' # in hours

    def generate_slurm_script(self, nodelist, steps, backend, caware, order, precision, nodes, ntasks , etype, elems, partition, gpu):

        # If the string nodelist contains the substring 'ac' then we are working on the ACES cluster
        # else if nodelist contains the substring 'fc' then we are working on the FASTER cluster
        if   'ac' in nodelist: cluster = 'ACES'
        elif 'fc' in nodelist: cluster = 'FASTER'
        else:                  raise ValueError(f"Cluster not supported")

        mpi_lib = 'mpich'   # Use MPICH everywhere
        #export MPIR_CVAR_ENABLE_GPU=1 ; 
        if   backend ==   'cuda': srun_or_mpirun = f'time mpirun  '
        elif backend == 'opencl': srun_or_mpirun = f'time mpirun '
        elif backend in ['hip', 'metal', 'openmp']: 
            raise ValueError(f"Backend {backend} yet to be supported")
        else: 
            raise ValueError(f"Backend {backend} DOES NOT EXIST!!")

        a100_subscripts = {
            'setup': f'/sw/local/bin/query_gpu.sh ; nvidia-smi -L ; clinfo -l',
            'run': f'CMD="{srun_or_mpirun} -n {ntasks} pyfr run -b {backend} $meshf $inif";\n'\
                     f'echo -e "\\nExecuting command:\\n==================\\n$CMD\\n";\n'\
                        f'eval $CMD;',
        }

        pvc_subscripts = {
            'setup': f'setup_custom_libraries_venv_{mpi_lib} ; clinfo -l',
            'run': f'xpumcli dump -d -1 -m 0,2,3,5,6,7,17,18 -i 10 > "log_gpus" &\n' \
                   f'xpumanager_pid=$!\n'\
                   f'CMD="time srun --mpi=pmi2 -n {ntasks} pyfr run -b {backend} $meshf $inif";\n'\
                   f'echo -e "\\nExecuting command:\\n==================\\n$CMD\\n"; \n'\
                   f'eval $CMD;\n'\
                   f'kill $xpumanager_pid'\
                    }

        h100_subscripts = {
            'setup': f'/sw/local/bin/query_gpu.sh ; nvidia-smi -L ; clinfo -l',
            'run': f'CMD="{srun_or_mpirun} -n {ntasks} pyfr run -b {backend} $meshf $inif";\n'\
                   f'echo -e "\\nExecuting command:\\n==================\\n$CMD\\n";\n'\
                   f'eval $CMD;',
        }

        # Options
        # 1.   aces, pvc,  pvc, opencl
        # 2.   aces, gpu, h100, opencl        
        # 3.   aces, gpu, h100,   cuda
        # 4. faster, gpu, a100, opencl
        # 5. faster, gpu, a100,   cuda

        if   partition == 'pvc' and gpu ==  'pvc': subscript_setup =  pvc_subscripts['setup']; subscript_run =  pvc_subscripts['run']
        elif partition == 'gpu' and gpu == 'h100': subscript_setup = h100_subscripts['setup']; subscript_run = h100_subscripts['run']
        elif partition == 'gpu' and gpu == 'a100': subscript_setup = a100_subscripts['setup']; subscript_run = a100_subscripts['run']
        elif partition == 'gpu' and gpu ==  'a40': subscript_setup = a100_subscripts['setup']; subscript_run = a100_subscripts['run']
        elif partition == 'gpu' and gpu ==  'a10': subscript_setup = a100_subscripts['setup']; subscript_run = a100_subscripts['run']
        elif partition == 'gpu' and gpu ==   't4': subscript_setup = a100_subscripts['setup']; subscript_run = a100_subscripts['run']
        else: raise ValueError(f"Partition {partition} not supported")

        job_name = f"{self.prefix}partition{partition}_nodelist{nodelist}_" \
                   f"steps{steps}_backend{backend}_caware{caware}_order{order}_precision{precision}_nodes{nodes}_" \
                   f"tasks{ntasks}_{etype}{elems}"

        return f'''#!/bin/bash
#SBATCH --job-name="{job_name}"
#SBATCH --nodes={nodes}
##SBATCH --exclusive
#SBATCH --reservation=benchmarking
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-{self.simulation_wait_time}:00:00
#SBATCH --mem=80G
#SBATCH --output={job_name}.out
#SBATCH --no-requeue
#SBATCH --partition={partition}
#SBATCH --ntasks={ntasks}
#SBATCH --gres=gpu:{gpu}:{int(np.ceil(ntasks/nodes))}
#SBATCH --cpus-per-gpu=8
##SBATCH --nodelist={nodelist}

source ~/.bashrc

add_all_paths

{subscript_setup}

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

echo $PATH

# Run subscript
{subscript_run}

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

    def make_scripts(self, npartition, nnodelist,  ngpu,
                           nsteps, nbackend, ncaware, norder, nprecision,
                           nnodes, ntasks_per_node, 
                           netype, nelements,):

        os.system("mkdir -p scripts")
        
        for nodelist, steps, backend, caware, order, precision, nodes, tasks_per_node, etype, elements, partition, gpu in zip(nnodelist, nsteps, nbackend, ncaware, norder, nprecision, nnodes, ntasks_per_node, netype, nelements, npartition, ngpu):

            tasks = nodes * tasks_per_node

            script = self.generate_slurm_script(nodelist, steps, backend, caware, order, precision, nodes, tasks, etype, elements, partition, gpu)
            output = f"scripts/{self.prefix}partition{partition}_gpu{gpu}_nodelist{nodelist}_steps{steps}_backend{backend}_caware{caware}_order{order}_precision{precision}_nodes{nodes}_tasks{tasks}_{etype}{elements}.sh"
            if not os.path.isfile(output):
                self.write_script_to_file(script, output)
                print(f"Script created: {output}")
            else:
                print(f"Script  exists: {output}")
