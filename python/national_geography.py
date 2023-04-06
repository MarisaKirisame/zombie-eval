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
    gimp_program = f"gdb --args {gimp_program}"

def timed(f):
    before  = datetime.now()
    f()
    after = datetime.now()
    return (after - before).total_seconds()

def ng():
    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_dir = f"log/{dt}"
    run(f"mkdir -p {log_dir}")
    os.chdir(log_dir)

    export_env_var()
    os.environ["USE_ZOMBIE"] = "1"

    run(f"cp {cwd}/picture/picture.jpeg ./")
    # we are measuring end to end time instead of cpu time,
    # because when it is swapping cpu is idling.
    used_time = timed(lambda: run(gimp_program + "|| true"))

    data = {}
    data["used_time"] = used_time
    with open('result.json', 'w') as f:
        json.dump(data, f)

    run("rm picture.jpeg")

    os.chdir(cwd)

    print(f"eval log written to {log_dir}")
    return dt

if __name__ == "__main__":
    ng()
