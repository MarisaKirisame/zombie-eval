from common import *

export_env_var()

programs = ['(elsamuko-national-geographic-batch "picture.jpeg" 60 1 60 25 0.4 1 0)',
            '(gimp-quit 0)']

run("cp picture/picture.jpeg ./")

run(f"_build/bin/gimp-2.10 -i " + " ".join(["-b " + "\'" + x + "\'" for x in programs]))

run("rm picture.jpeg")
