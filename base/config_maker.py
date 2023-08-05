import os
import configparser

class MyConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

class ConfigMaker:
    def __init__(self, prefix=''):
        self.prefix = prefix

    def create_config(self, number_of_timesteps, mpi_type, output_file, partition_file):
        # Calculate values based on input
        tend = number_of_timesteps * 1e-4
        
        # Create and configure the configparser object
        config = MyConfigParser()
        config.optionxform = str  # Preserve case sensitivity

        config["backend"] = {
            "precision": "double",
            "rank-allocator": "linear",
            "collect-wait-times": "true",
        }
        config["backend-cuda"] = {
            "device-id": "local-rank",
            "mpi-type": "cuda-aware",
            "block-1d": "64",
            "block-2d": "128",
        }
        config["constants"] = {
            "gamma": "1.4",
            "mu": "7.395099728874521e-05",
            "Pr": "0.71",
            "M": "0.1",
        }
        config["solver"] = {
            "system": "navier-stokes",
            "order": "3",
            "anti-alias": "none",
            "viscosity-correction": "none",
            "shock-capturing": "none",
        }
        config["solver-time-integrator"] = {
            "scheme": "rk4",
            "controller": "none",
            "tstart": "0",
            "tend": f"{tend:.2f}",  # Format tend to 2 decimal places
            "dt": "1e-4",
        }
        config["solver-interfaces"] = {
            "riemann-solver": "rusanov",
            "ldg-beta": "0.5",
            "ldg-tau": "0.1",
        }
        config["solver-interfaces-quad"] = {
            "flux-pts": "gauss-legendre",
            "quad-deg": "6",
            "quad-pts": "gauss-legendre",
        }
        config["solver-elements-hex"] = {
            "soln-pts": "gauss-legendre",
            "quad-deg": "6",
            "quad-pts": "gauss-legendre",
        }
        config["soln-ics"] = {
            "u": "+0.118321595661992*sin(x)*cos(y)*cos(z)",
            "v": "-0.118321595661992*cos(x)*sin(y)*cos(z)",
            "w": "0.0",
            "p": "1.0+1.0*0.118321595661992*0.118321595661992/16*(cos(2*x)+cos(2*y))*(cos(2*z)+2)",
            "rho": "(1.0+1.0*0.118321595661992*0.118321595661992/16*(cos(2*x)+cos(2*y))*(cos(2*z)+2))/1.0",
        }
        config["soln-plugin-benchmark"] = {
            "flushsteps": "1",
            "file": "perf.csv",
            "header": "true",
            "mesh": partition_file,
            "continue-sim": "False",
        }

        # Modify values if provided
        if mpi_type == 0:
            config["backend-cuda"]["mpi-type"] = 'standard'
        elif mpi_type == 1:
            config["backend-cuda"]["mpi-type"] = 'cuda-aware'
        else:
            raise ValueError("mpi-type value must be 0 or 1")

        # Write the config file
        with open(output_file, 'w') as configfile:
            config.write(configfile)

    def make_configs(self, nsteps, caware, nparts, nelems, partition_dir = 'partitions'):
        
        os.system("mkdir -p configs")

        for steps, cuda, npart, nelem in zip(nsteps, caware, nparts, nelems):

            # Echo the current configuration
            print(f"steps: {steps}, cuda: {cuda}")
            config=f"configs/{self.prefix}steps{steps}_caware{cuda}_parts{npart}_elems{nelem}.ini"
            partition_file = f'../../{partition_dir}/parts{npart}_elems{nelem}.pyfrm'

            if not os.path.isfile(config):
                self.create_config(steps, cuda, config, partition_file)
                print(f"Config created: {config}")
            else:
                print(f"Config  exists: {config}")
