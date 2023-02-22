'''
Unless explictly mentioned all paths are with respect to the directory of execution of this script.
'''

CHAMPSIM_SOURCE_FOLDER = "../ChampSim"
BINARY_STORE_FOLDER = "bin"  # Defined with respect to CHAMPSIM_SOURCE_FOLDER
RESULTS_STORE_FOLDER = "results"  
CONFIG_FILE_STORE = f"{CHAMPSIM_SOURCE_FOLDER}/configs"
EXPERIMENTS_JSON = "experiments.json"
NUM_OF_PROCESSES_IN_ONE_GO = 2
TRACES_DIR = f"{CHAMPSIM_SOURCE_FOLDER}/traces"
WARMUP_INSTRUCTIONS = 200000000
SIMULATION_INSTRUCTIONS = 1000000000
SLEEP_TIME_FOR_POLLING = 5 # in seconds