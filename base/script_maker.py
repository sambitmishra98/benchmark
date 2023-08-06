import os
import numpy as np

class ScriptMaker:
    def __init__(self, prefix = ''):

        self.prefix = prefix
        self.venv_bin_path = "/scratch/user/sambit98/virtual-environments/benchmark/bin/"
        self.benchmark_path = "/scratch/user/sambit98/BENCHMARK/benchmarking/"
        self.simulation_wait_time = '30' # in minutes

    def generate_slurm_script(self, nodelist, time_steps, c, nodes, nparts, elems,):
        job_name = f"{self.prefix}nodelist{nodelist}_steps{time_steps}_caware{c}_nodes{nodes}_tasks{nparts}_elems{elems}"
        
        return f'''#!/bin/bash
#SBATCH -J "{job_name}"
#SBATCH --ntasks={nparts}
#SBATCH --gres=gpu:a100:{int(np.ceil(nparts/nodes))}
#SBATCH --nodes={nodes}
##SBATCH --exclusive
#SBATCH --cpus-per-gpu=2
#SBATCH --gpu-bind=closest
#SBATCH --use-min-nodes
#SBATCH --time=0-00:{self.simulation_wait_time}:00
#SBATCH --output={job_name}.out
#SBATCH --no-requeue
#SBATCH -p gpu
#SBATCH --mem=600G
#SBATCH --nodelist={nodelist}

module purge

/sw/local/bin/query_gpu.sh

local=/scratch/user/sambit98/.local/
export            PATH=$local/bin/:$PATH
export           CPATH=$local/include/:$CPATH
export          CPPATH=$local/include/:$CPPATH
export          LDPATH=$local/lib/:$LDPATH
export    LIBRARY_PATH=$local/lib/:$LIBRARY_PATH
export LD_LIBRARY_PATH=$local/lib/:$LD_LIBRARY_PATH

module load foss/2022b
module load UCX-CUDA/1.13.1-CUDA-11.8.0
module load libffi/3.4.4
module load OpenSSL/1.1.1n
module load METIS/5.1.0
module load HDF5/1.14.0
module load SQLite/3.39.4
module load bzip2/1.0.8

. {self.venv_bin_path}activate

numnodes=$SLURM_JOB_NUM_NODES
mpi_tasks_per_node=$(echo "$SLURM_TASKS_PER_NODE" | sed -e  's/^\([0-9][0-9]*\).*$/\\1/')
np=$[${{SLURM_JOB_NUM_NODES}}*${{mpi_tasks_per_node}}]

python_runner="{self.venv_bin_path}python3"
pyfr_runner="{self.venv_bin_path}pyfr"

cd     "{self.benchmark_path}"
inif="{self.benchmark_path}configs/steps{time_steps}_caware{c}_parts{nparts}_elems{elems}.ini"
meshf="{self.benchmark_path}partitions/parts{nparts}_elems{elems}.pyfrm"; 

echo "Running on master node: `hostname`"
echo "Time: `date`"
echo "Current directory: `pwd`"
echo -e "JobID: $SLURM_JOB_ID\\n======"
echo -e "\\nnumtasks=${{SLURM_NTASKS}}, numnodes=${{SLURM_JOB_NUM_NODES}}, mpi_tasks_per_node=${{mpi_tasks_per_node}} (OMP_NUM_THREADS=$OMP_NUM_THREADS)"

mkdir -p {self.benchmark_path}solns/{self.prefix}nodelist{nodelist}_steps{time_steps}_caware{c}_nodes{nodes}_tasks{nparts}_elems{elems};
cd       {self.benchmark_path}solns/{self.prefix}nodelist{nodelist}_steps{time_steps}_caware{c}_nodes{nodes}_tasks{nparts}_elems{elems}; 


nvidia-smi --query-gpu=index,name,pci.bus,persistence_mode,timestamp,pstate,utilization.gpu,utilization.memory --format=csv -l 5 -f log_gpus.csv &
nvidia_smi_pid=$!

# nvidia-smi dmon -o DT -d 10 -s ut > "log_gpus" &
##  nsys profile --output=pyfr_profile.qdrep --trace=cuda,nvtx,osrt

CMD="time mpirun -n {nparts} $python_runner $pyfr_runner run -b cuda $meshf $inif"; 
echo -e "\\nExecuting command:\\n==================\\n$CMD\\n"; echo "Time: `date`"

eval $CMD;

kill $nvidia_smi_pid

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

    def make_scripts(self, nodelist, nsteps, caware, nnodes,   ntasks_per_node, nelements, ):

        os.system("mkdir -p scripts")
        
        for nodelist, time_steps, c, nodes, tasks_per_node, elements in zip(nodelist, nsteps, caware, nnodes, ntasks_per_node, nelements):

            tasks = nodes * tasks_per_node

            script = self.generate_slurm_script(nodelist, time_steps, c, nodes, tasks, elements)
            output = f"scripts/{self.prefix}nodelist{nodelist}_steps{time_steps}_caware{c}_nodes{nodes}_tasks{tasks}_elems{elements}.sh"
            if not os.path.isfile(output):
                self.write_script_to_file(script, output)
                print(f"Created script: {output}")
            else:
                print(f"Script exists at : {output}")
