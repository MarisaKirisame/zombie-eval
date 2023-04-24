import json
import os
from national_geographic import *
from common import *
from os import sys
import dominate
from dominate.tags import *

class page(dominate.document):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def _add_to_ctx(self):
        pass # don't add to contexts

    def __exit__(self, *args):
        super().__exit__(*args)
        with open(str(self.path), "w") as f:
            f.write(str(self))

def nightly(dry):
    cwd = os.getcwd()

    dt = ng()

    out_dir = f"{cwd}/out"
    out_dir_dt = f"{cwd}/out/{dt}"

    log_dir = f"{cwd}/log"
    log_dir_dt = f"{cwd}/log/{dt}"

    with open(f'{log_dir_dt}/result.json') as f:
        data = json.load(f)

    run(f"mkdir -p {out_dir_dt}")
    os.chdir(out_dir_dt)

    with page(path=f"index.html", title="nightly") as doc:
        p(f"baseline_used_time = {data['baseline_used_time']}")
        p(f"zombie_used_time = {data['zombie_used_time']}")
        p(f"diff = {data['diff']}")
        run(f"cp {log_dir_dt}/baseline.jpeg ./")
        run(f"cp {log_dir_dt}/zombie.jpeg ./")
        run(f"cp {log_dir_dt}/delta.jpeg ./")
        img(src="baseline.jpeg")
        p("baseline")
        img(src="zombie.jpeg")
        p("zombie")
        img(src="delta.jpeg")
        p("delta")

    os.chdir(out_dir)

    if dry:
        run(f"xdg-open {dt}/index.html")
    else:
        run(f"nightly-results publish {dt}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        assert sys.argv[1] == "dry-run"
        nightly(dry=True)
    else:
        assert len(sys.argv) == 1
        nightly(dry=False)
