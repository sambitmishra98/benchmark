import subprocess
import os
import pandas as pd

c = pd.DataFrame( 
               [
#                ['fc024', 2000,     1,                     1,    1,             32, ],
#                ['fc024', 2000,     1,                     1,    2,             40, ],
#                ['fc024', 2000,     1,                     1,    4,             51, ],
#                ['fc024', 2000,     1,                     1,    6,             58, ],
#                ['fc024', 2000,     1,                     1,    8,             64, ],
#                ['fc024', 2000,     1,                     1,   10,             69, ],
#                ['fc024', 2000,     1,                     1,   12,             73, ],
#                ['fc024', 2000,     1,                     1,   14,             77, ],
#                ['fc024', 2000,     1,                     1,   16,             81, ],
#                ['fc024', 2000,     1,                     1,    1,             64, ],
#                ['fc024', 2000,     1,                     1,    2,             81, ],
#                ['fc024', 2000,     1,                     1,    4,            102, ],
#                ['fc024', 2000,     1,                     1,    6,            116, ],
#                ['fc024', 2000,     1,                     1,    8,            128, ],
#                ['fc024', 2000,     1,                     1,   10,            138, ],
#                ['fc024', 2000,     1,                     1,   12,            147, ],
#                ['fc024', 2000,     1,                     1,   14,            154, ],
#                ['fc024', 2000,     1,                     1,   16,            161, ],
#                ['fc024', 2000,     1,                     1,    1,             96, ],
#                ['fc024', 2000,     1,                     1,    2,            121, ],
#                ['fc024', 2000,     1,                     1,    4,            152, ],
#                ['fc024', 2000,     1,                     1,    6,            174, ],
#                ['fc024', 2000,     1,                     1,    8,            192, ],
#                ['fc024', 2000,     1,                     1,   10,            207, ],
#                ['fc024', 2000,     1,                     1,   12,            220, ],
#                ['fc024', 2000,     1,                     1,   14,            231, ],
#                ['fc024', 2000,     1,                     1,   16,            242, ],

#                 ['fc004',  2000,   1,                     1,    1,            96, ],
                ['fc026', 100,   1,                     1,   1,              96, ],
#                ['fc004', 10,   1,                     1,   16,            242, ],

                ], 

    columns=['nodelist', 'nsteps', 'caware','nnodes', 'nparts-per-node', 'nelements', ])

def submit_job(job_script):

    try:
        # Submit the job using sbatch
        f = subprocess.run(['sbatch', job_script], check=True , capture_output=True, text=True)

        print(f)

        # Get the Job ID
        job_id = f.stdout.split()[-1]
        return job_id

    except Exception as e:
        print(f"An error occurred while submitting {job_script}: {e}")

if __name__ == "__main__":

    prefix = ''

    base_dir = "/scratch/user/sambit98/BENCHMARK/benchmarking/"
    soln_dir   = base_dir + "solns/"
    script_dir = base_dir + "scripts/"
    
    # List to store all the Job IDs
    job_ids = []
    
    # Iterate over the list of scripts and submit each one
    for        nodelist,       nsteps,        caware,       nnodes,       ntasks,              nelements in  \
    zip(    c['nodelist'],  c['nsteps'],   c['caware'],  c['nnodes'],  c['nparts-per-node'],c['nelements']):
        sbatch_script = f"{prefix}nodelist{nodelist}_steps{nsteps}_caware{caware}_nodes{nnodes}_tasks{ntasks*nnodes}_elems{nelements}.sh"

        script_name = os.path.basename(sbatch_script)

        # The directory name is the same as the script name without the extension
        job_directory = script_name.split('.')[0]

        print(f"Checking if the directory for {script_name} exists...")

        # Check if the directory has been created, if not then submit the job
        if not os.path.exists(soln_dir+job_directory):

            # Go into the directory where the script is located
            os.chdir(script_dir)
            job_id = submit_job(script_dir+sbatch_script)
            os.chdir(base_dir)

            # Append the Job ID to the list
            with open(f"{prefix}nodelist{nodelist}_steps{nsteps}_caware{caware}_nodes{nnodes}__job_ids_{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", 'a') as file:
                file.write(f"tasks{ntasks*nnodes}_elems{nelements},{job_id}\n")

            job_ids.append(job_id)
            print(f"Job {sbatch_script} submitted successfully with Job ID: {job_id}")
        else:
            print(f"The directory for {script_name} already exists, skipping the submission.")
