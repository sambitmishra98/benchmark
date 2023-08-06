# Benchmarking with PyFR on cluster
This repository contains Python scripts that automate the setup, execution, and post-processing of PyFR in a High Performance Computing (HPC) environment, specifically a cluster running the Slurm Workload Manager. 

The `benchmark` branch in `https://github.com/sambitmishra98/PyFR.git` is used to run the experiments

# Workflow

The workflow consists of three steps, each corresponding to a Python script:
1. preprocess.py
2. run.py
3. postprocess.py

## Preprocessing (preprocess.py)
This script prepares the environment for running a set of experiments. 
Before running the preprocess.py script, the user should edit the variable `c` in preprocess.py and run.py

Several helper classes are used in this stage:

- `ConfigMaker`: Generates the necessary configuration files for each experiment.
- `MeshMaker`: Creates meshes, each with a specified number of elements.
- `PartitionMaker`: Creates partitions based on the number of nodes and tasks per node.
- `ScriptMaker`: Generates scripts to run each of the experiments.

After running the script, user must look at the generated files and make sure that the configurations are correct.

## Running Jobs (run.py)
This script manages the submission of jobs to the Slurm queue. 
It iterates over all the configurations, creates a script name for each, and checks if a directory for that script name already exists. 
If the directory does not exist, the corresponding job is submitted to the Slurm queue via the sbatch command, and the returned job ID is stored for future reference.

This script also records the job IDs in a text file, which can be used for tracking or auditing purposes.

Note: This script checks for the existence of a directory for each script and, if it finds one, assumes the experiment has already been run and does not resubmit the job. 
If an experiment needs to be rerun, the corresponding output directory should be manually deleted.

## Post-processing (postprocess.py)

Once all jobs have completed, this script gathers and processes the data from the output files. 
It traverses the output directories, parses relevant information from the output files, and computes performance metrics based on the time elapsed during the experiments.

These metrics are then written into a .csv file in the respective output directory. 
Finally, the script consolidates all of this data into a single .csv file.

Usage:

    python postprocess.py

In summary, this workflow allows for the efficient setup, execution, and analysis of HPC experiments. 
By leveraging Python's scripting capabilities and Slurm's job scheduling, it streamlines the process of running a series of experiments on a compute cluster.

## Past simulations

All of the simulations performed previously are stored as `ROUND-#` folders. 

## Finding Job IDs

The job IDs generated from submitting tasks to the Slurm queue are stored in text files in the base directory. The filename follows this pattern:

nodelist{NODELIST}_steps{NSTEPS}_samples{NSAMPLES}_caware{CAWARE}_nodes{NNODES}__job_ids_{TIMESTAMP}.txt

The placeholders {NODELIST}, {NSTEPS}, {NSAMPLES}, {CAWARE}, and {NNODES} correspond to the configuration parameters for each experiment, and {TIMESTAMP} is the date and time at which the file was created, formatted as %Y-%m-%d_%H-%M-%S.

So, for example, if an experiment was run with a nodelist of ac024, 20000 steps, 4 samples, caware of 1, and 16 nodes, and this experiment was run on May 26, 2023 at 14:30:15, the job ID would be saved in a file named:

    nodelistac024_steps20000_samples4_caware1_nodes16__job_ids_2023-05-26_14-30-15.txt

These files will be located in the same directory where you run the run.py script.
