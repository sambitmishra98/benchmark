import subprocess
import os
import pandas as pd

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


    c = pd.read_csv('configurations.csv', comment='#', 
                    dtype={'nodelist':str, 
                           'nsteps':int, 'backend':str, 'caware':int, 'order':int, 'precision':str,
                           'nnodes':int, 'nparts-per-node':int, 
                           'etype':str, 'nelements':int, 
                           'partition':str, 'gpu':str
                           },
                    skipinitialspace=True,
                    )

    prefix = ''

    
    # List to store all the Job IDs
    job_ids = []
    
    # Iterate over the list of scripts and submit each one
    for        partition,     gpu,     nodelist,       nsteps,      backend,         caware,      order,        precision,       nnodes,       ntasks,              etype,     nelements,  in  \
    zip(    c['partition'],c['gpu'],c['nodelist'],  c['nsteps'], c['backend'],    c['caware'], c['order'],   c['precision'],  c['nnodes'],  c['nparts-per-node'],c['etype'],c['nelements'],):

        if   'ac' in nodelist: 
            cluster = 'ACES'
            base_dir = "/scratch/user/u.sm121949/EFFORT_BENCHMARK/benchmark/"
    
        elif 'fc' in nodelist: 
            cluster = 'FASTER'
            base_dir = "/scratch/user/sambit98/EFFORT_BENCHMARK/benchmark/"
        else:                  raise ValueError(f"Cluster not supported")

        soln_dir   = base_dir + "solns/"
        script_dir = base_dir + "scripts/"

        sbatch_script = f"{prefix}partition{partition}_gpu{gpu}_nodelist{nodelist}_steps{nsteps}_backend{backend}_caware{caware}_order{order}_precision{precision}_nodes{nnodes}_tasks{ntasks*nnodes}_{etype}{nelements}.sh"

        script_name = os.path.basename(sbatch_script)

        # The directory name is the same as the script name without the extension
        job_directory = script_name.split('.')[0]

        print(f"Does the directory for {script_name} exist? \t", end="")

        # Check if the directory has been created, if not then submit the job
        if not os.path.exists(soln_dir+job_directory):
            print("NO")
            # Create the directory and go there.
            os.makedirs(soln_dir+job_directory)
            os.chdir(soln_dir+job_directory)

            job_id = submit_job(script_dir+sbatch_script)

            # Append the Job ID to the list
            with open(f"{prefix}partition{partition}_gpu{gpu}_steps{nsteps}_backend{backend}_caware{caware}_order{order}_precision{precision}_job_ids_{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M')}.txt", 'a') as file:
                file.write(f"nodelist{nodelist}_nodes{nnodes}_tasks{ntasks*nnodes}_{etype}{nelements},{job_id}\n")

            os.chdir(soln_dir)
            job_ids.append(job_id)

            print(f"Job ID: {job_id} \t script: {sbatch_script}")
        else:
            print(f"YES! SKIPPING SIMULATION! The directory for {script_name} already exists. Delete it to resubmit the job.")
