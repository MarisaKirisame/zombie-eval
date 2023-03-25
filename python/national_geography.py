from common import *
import os

export_env_var()

os.environ["USE_ZOMBIE"] = "1"

programs = ['(elsamuko-national-geographic-batch "picture.jpeg" 60 1 60 25 0.4 1 0)',
            '(gimp-quit 0)']

run("cp picture/picture.jpeg ./")

gimp_program = f"_build/bin/gimp-2.10 -i " + " ".join(["-b " + "\'" + x + "\'" for x in programs])

DEBUG = False

if DEBUG:
    gimp_program = f"gdb --args {gimp_program}"

run(gimp_program + "|| true")

run("rm picture.jpeg")
