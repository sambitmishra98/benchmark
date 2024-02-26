import os
import numpy as np
import configparser

# Get the following as optional arguments
BENCHMARK_WITH_SOLUTION_FILE = True
BENCHMARK_WITH_PROFILE=False
BENCHMARK_WITH_CLBLAST = False
BENCHMARK_FIRST_ACCELERATOR = True

class MyConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

class ConfigMaker:
    def __init__(self, prefix=''):
        self.prefix = prefix

    def create_config(self, number_of_timesteps, output_file, aware, order, precision, partition_file):
        # Calculate values based on input

        # number_of_timesteps is always a power of 10. So let us get the exponent
        # of the power of 10
        expo = int(np.log10(number_of_timesteps))

        expo_dt = expo-4

        dt = 1e-4
        tend = 0.0001 + 10**(expo_dt)

        # Create and configure the configparser object
        config = MyConfigParser()
        config.optionxform = str  # Preserve case sensitivity

        config["backend"] = {
            "precision": precision,
            "rank-allocator": "linear",
            "collect-wait-times": "true",
            "memory-model": "large",
        }
        config["backend-cuda"] = {
            "device-id": "0" if BENCHMARK_FIRST_ACCELERATOR else "local-rank",
            "mpi-type": "cuda-aware" if aware else "standard",
        }
        config["backend-hip"] = {
            "device-id": "0" if BENCHMARK_FIRST_ACCELERATOR else "local-rank",
            "mpi-type": "hip-aware" if aware else "standard",
        }
        config["backend-opencl"] = {
            "platform-id": "0",
            "device-type": "GPU",
            "device-id"  : "0" if BENCHMARK_FIRST_ACCELERATOR else "local-rank",                     
            "gimmik-max-nnz": "4" if BENCHMARK_WITH_CLBLAST else "100000000",
        }
        config["constants"] = {
            "gamma": "1.4",
            "mu": "7.395099728874521e-05",
            "Pr": "0.71",
            "M": "0.1",
            "U": "0.118321595661992",
        }
        config["solver"] = {
            "system": "navier-stokes",
            "order": order,
            "anti-alias": "none",
            "viscosity-correction": "none",
            "shock-capturing": "none",
        }

        if BENCHMARK_WITH_SOLUTION_FILE:
            config["solver-time-integrator"] = {
                "scheme": "rk4",
                "controller": "none",
                "tstart": "0",
                "tend": f"{tend:.4f}",  # Format tend to 2 decimal places
                "dt": f"{dt:.4f}",
            }                
        else:
            config["solver-time-integrator"] = {
                "scheme": "rk45",
                "controller": "pi",
                "tstart": "0",
                "tend": f"{tend:.4f}",  # Format tend to 2 decimal places
                "dt": f"{dt:.4f}",
                "atol": "0.000001",
                "rtol": "0.000001",
                "safety-fact": "0.9",
                "min-fact": "0.3",
                "max-fact": "2.5",
            }

        config["solver-interfaces"] = {
            "riemann-solver": "rusanov",
            "ldg-beta": "0.5",
            "ldg-tau": "0.1",
        }
        config["solver-elements-tet"] = {
            "soln-pts": "shunn-ham",
            "quad-deg": "6",
            "quad-pts": "shunn-ham",
        }

        config["solver-elements-pyr"] = {
            "soln-pts": "gauss-legendre",
            "quad-deg": "6",
            "quad-pts": "witherden-vincent",
        }

        config["solver-elements-pri"] = {
            "soln-pts": "williams-shunn~gauss-legendre",
            "quad-deg": "6",
            "quad-pts": " williams-shunn~gauss-legendre",
        }

        config["solver-elements-hex"] = {
            "soln-pts": "gauss-legendre",
            "quad-deg": "6",
            "quad-pts": "gauss-legendre",
        }
        config["solver-interfaces-tri"] = {
            "flux-pts": "williams-shunn",
            "quad-deg": "6",
            "quad-pts": "williams-shunn",
        }
        config["solver-interfaces-quad"] = {
            "flux-pts": "gauss-legendre",
            "quad-deg": "6",
            "quad-pts": "gauss-legendre",
        }
        config["soln-ics"] = {
            "u": "+U*sin(x)*cos(y)*cos(z)",
            "v": "-U*cos(x)*sin(y)*cos(z)",
            "w": "0.0",
            "p": "1.0+1.0*U*U/16*(cos(2*x)+cos(2*y))*(cos(2*z)+2)",
            "rho": "(1.0+1.0*U*U/16*(cos(2*x)+cos(2*y))*(cos(2*z)+2))/1.0",
        }
        if not BENCHMARK_WITH_PROFILE:        
#            config["soln-plugin-benchmark"] = {
#                "flushsteps": "10000",
#                "file": "perf_counter_measurements.csv",
#                "header": "true",
#                "mesh": partition_file,
#                "continue-sim": "True",
#            }
            config["soln-plugin-writer"] = {
                "dt-out": str(10**expo_dt),
                "basedir": ".",
                "basename": f"soln-{{t:.{-expo_dt}f}}",
            }

#        config["soln-plugin-integrate"] = {
#            "nsteps": "1000",
#            "file": "integral.csv",
#            "header": "true",
#            "vor1": "(grad_w_y - grad_v_z)",
#            "vor2": "(grad_u_z - grad_w_x)",
#            "vor3": "(grad_v_x - grad_u_y)",
#
#            "int-E": "rho*(u*u + v*v + w*w)",
#            "int-enst": "rho*(%(vor1)s*%(vor1)s + %(vor2)s*%(vor2)s + %(vor3)s*%(vor3)s)",
#        }
#        config["soln-plugin-sampler"] = {
#            "nsteps": "1000",
#            "samp-pts": "[(1.0, 1.0, 1.0),]",
#            "format": "primitive",
#            "file": "sampler.csv",
#            "header": "true",
#        }
#        config["soln-plugin-dtstats"] = {
#            "flushsteps": "1000",
#            "file": "dtstats.csv",
#            "header": "true",
#        }
#        config["soln-plugin-residual"] = {
#            "nsteps": "1000",
#            "file": "residual.csv",
#            "header": "true",
#        }

        # Write the config file
        with open(output_file, 'w') as configfile:
            config.write(configfile)

    def make_configs(self, nsteps, ncaware, norder, nprecision,
                           nparts, 
                           netype, nelems, ):

        os.system("mkdir -p configs")

        for steps, aware, order, precision, npart, etype, nelem in zip(nsteps, ncaware, norder, nprecision, nparts, netype, nelems):

            # Echo the current configuration
            print(f"steps: {steps}")
            config=f"configs/{self.prefix}steps{steps}_caware{aware}_order{order}_precision{precision}_tasks{npart}_{etype}{nelem}.ini"
            partition_file = f'../../partitions/tasks{npart}_{etype}{nelem}.pyfrm'

            if not os.path.isfile(config):
                self.create_config(steps, config, aware, order, precision, partition_file)
                print(f"Config created: {config}")
            else:
                print(f"Config  exists: {config}")
