import subprocess
import constants
import json

class Experiment:
    def __init__(self, name,config_path):
        self.name = name
        self.config_path = config_path


def generate_config_file(expt_name,replacement=None,branch=None,btb=None,prefetcher=None):
    """
        Generates the config files for different experiments
    """
    with open(f"{constants.CHAMPSIM_SOURCE_FOLDER}/champsim_config.json","r") as f:
        data = json.load(f)
    if(replacement != None):
        data["LLC"]["replacement"] = replacement
    if(branch != None):
        data["ooo_cpu"]["branch_predictor"] = branch
    if(btb != None):
        data["ooo_cpu"]["btb"] = btb
    if(prefetcher != None):
        data["ooo_cpu"]["prefetcher"] = prefetcher
    path = f"{constants.CONFIG_FILE_STORE}/{expt_name}_config.json"
    with open(path,"w") as f:
        f.write(json.dumps(data))
    return path
    

        

def generate_binaries(experiments):
    """
        Generates the binaries for the experiments.
    """
    
    for experiment in experiments:        
        subprocess.call([f"config.sh",experiment.config_path],cwd=constants.CHAMPSIM_SOURCE_FOLDER)
        with open("Makefile","rw") as f:
            content = f.read().replace("bin/champsim",f"{constants.BINARY_STORE_FOLDER}/expt_{experiment.name}_bin")
            f.write(content)
        print(f"Building binary for experiment {experiment.name}...")
        print("=================================================")
        subprocess.call(["make"],cwd=constants.CHAMPSIM_SOURCE_FOLDER)
        print("=================================================")
        
        

def get_experiments():
    experiments_list = []
    with open("experiments.json","r") as f:
        experiments = json.load(f)
        for experiment in experiments:
            replacement = None
            branch = None
            btb = None
            prefetcher = None

            if ("replacement" in experiment):
                replacement = experiment["replacement"]
            if ("branch" in experiment):
                branch = experiment["branch"]
            if ("btb" in experiment):
                btb = experiment["btb"]          
            if ("prefetcher" in experiment):
                prefetcher = experiment["prefetcher"]
            experiments_list.append(Experiment(name=experiment["name"],config_path=generate_config_file(experiment["name"],replacement=replacement,branch=branch,btb=btb,prefetcher = prefetcher)))
            
  