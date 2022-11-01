import subprocess
import constants
import json
import os
import time

class Experiment:
    def __init__(self, name, config_path):
        self.name = name
        self.config_path = config_path
        self.binary_path = None
        


def schedule_experiments(experiments):
    processes = []
    for experiment in experiments:
        if experiment.binary_path == None:
            print(f"Warning: Experiment's binary {experiment.name} was not found")
            continue
        traces = os.listdir(constants.TRACES_DIR)
        for trace in traces:
            directory = f"{constants.RESULTS_STORE_FOLDER}/results_{experiment.name}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            processes.append(
                {
                    "proc_name": experiment.name+f" (Trace: {trace})",
                    "command": f"{experiment.binary_path} --warmup_instructions {constants.WARMUP_INSTRUCTIONS} --simulation_instructions {constants.SIMULATION_INSTRUCTIONS} traces/{trace}",
                    "result_file": f"{directory}/{trace}_summary.txt",
                }
            )
    for i in range(0, len(processes), constants.NUM_OF_PROCESSES_IN_ONE_GO):
        currently_running = []
        print("=================================")
        for j in range(i, min(i + constants.NUM_OF_PROCESSES_IN_ONE_GO,len(processes))):
            f = open(processes[j]["result_file"], "w")
            print(f"Now running {processes[j]['proc_name']} ")
            currently_running.append(
                subprocess.Popen(processes[j]["command"].split(), stdout=f, stderr=f, cwd=constants.CHAMPSIM_SOURCE_FOLDER)
            )
        all_completed = False
        while not all_completed:
            all_completed = True
            for subproc in currently_running:
                poll = subproc.poll()
                if poll is None:
                    all_completed = False
                    time.sleep(constants.SLEEP_TIME_FOR_POLLING)
                    break
                    


def generate_config_file(
    expt_name, replacement=None, branch=None, btb=None, prefetcher=None
):
    """
    Generates the config files for different experiments
    """
    with open(f"{constants.CHAMPSIM_SOURCE_FOLDER}/champsim_config.json", "r") as f:
        data = json.load(f)
    if replacement != None:
        data["LLC"]["replacement"] = replacement
    if branch != None:
        data["ooo_cpu"]["branch_predictor"] = branch
    if btb != None:
        data["ooo_cpu"]["btb"] = btb
    if prefetcher != None:
        data["ooo_cpu"]["prefetcher"] = prefetcher
    path = f"{constants.CONFIG_FILE_STORE}/{expt_name}_config.json"
    with open(path, "w") as f:
        f.write(json.dumps(data))
    return path


def generate_binaries(experiments):
    """
    Generates the binaries for the experiments.
    """

    for experiment in experiments:
        bin_path = f"{constants.BINARY_STORE_FOLDER}/expt_{experiment.name}_bin"
        if os.path.isfile(f"{constants.CHAMPSIM_SOURCE_FOLDER}/{bin_path}"):
            print("Skipping binary generation for experiment", experiment.name)
            experiment.binary_path = bin_path
            continue
        subprocess.call(
            [f"./config.sh", experiment.config_path],
            cwd=constants.CHAMPSIM_SOURCE_FOLDER,
        )

        with open(f"{constants.CHAMPSIM_SOURCE_FOLDER}/Makefile", "r") as f:
            content = f.read().replace("bin/champsim", bin_path)
        with open(f"{constants.CHAMPSIM_SOURCE_FOLDER}/Makefile", "w") as f:
            f.write(content)
        print(f"Building binary for experiment {experiment.name}...")
        print("=================================================")
        subprocess.call(["make"], cwd=constants.CHAMPSIM_SOURCE_FOLDER)
        print("=================================================")
        experiment.binary_path = bin_path


def get_experiments():
    experiments_list = []
    with open("experiments.json", "r") as f:
        experiments = json.load(f)
        for experiment in experiments:
            replacement = None
            branch = None
            btb = None
            prefetcher = None

            if "replacement" in experiment:
                replacement = experiment["replacement"]
            if "branch" in experiment:
                branch = experiment["branch"]
            if "btb" in experiment:
                btb = experiment["btb"]
            if "prefetcher" in experiment:
                prefetcher = experiment["prefetcher"]
            experiments_list.append(
                Experiment(
                    name=experiment["name"],
                    config_path=generate_config_file(
                        experiment["name"],
                        replacement=replacement,
                        branch=branch,
                        btb=btb,
                        prefetcher=prefetcher,
                    ),
                )
            )
    return experiments_list


if __name__ == "__main__":
    experiments = get_experiments()
    generate_binaries(experiments)
    schedule_experiments(experiments)
