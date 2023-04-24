from common import *
import os
from datetime import datetime
import json

programs = ['(elsamuko-national-geographic-batch "picture.jpeg" 60 1 60 25 0.4 1 0)',
            '(gimp-quit 0)']

DEBUG = False

cwd = os.getcwd()

gimp_program = f"{cwd}/_build/bin/gimp-2.10 -i " + " ".join(["-b " + "\'" + x + "\'" for x in programs])

if DEBUG:
    gimp_program = f"gdb -return-child-result -ex='set confirm on' -ex=run -ex=quit --args {gimp_program}"
    #gimp_program = f"valgrind {gimp_program}"

def timed(f):
    before  = datetime.now()
    f()
    after = datetime.now()
    return (after - before).total_seconds()

os.environ["GEGL_THREADS"] = "1"

def set_zombie(use):
    os.environ["USE_ZOMBIE"] = "1" if use else "0"

def use_zombie():
    set_zombie(True)

def unuse_zombie():
    set_zombie(False)

def run_single_eval(name, data):
    run(f"cp {cwd}/picture/picture.jpeg ./")
    # we are measuring end to end time instead of cpu time,
    # because when it is swapping cpu is idling.
    used_time = timed(lambda: run(gimp_program + "|| true"))

    print(f"running {name} take {used_time}")
    data[f"{name}_used_time"] = used_time
    run(f"mv picture.jpeg {name}.jpeg")

def ng():
    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log_dir = f"log/{dt}"
    run(f"mkdir -p {log_dir}")
    os.chdir(log_dir)

    export_env_var()

    data = {}

    unuse_zombie()
    run_single_eval("baseline", data)

    use_zombie()
    run_single_eval("zombie", data)

    data["diff"] = float(query("compare -metric phash baseline.jpeg zombie.jpeg delta.jpeg 2>&1 || true"))

    run(f"cp {cwd}/picture/picture.jpeg ./original.jpeg")

    with open('result.json', 'w') as f:
        json.dump(data, f)

    os.chdir(cwd)

    print(f"eval log written to {log_dir}")
    return dt

if __name__ == "__main__":
    ng()
