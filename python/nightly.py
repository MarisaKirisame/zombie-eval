import json
import os
from national_geography import *
from common import *

cwd = os.getcwd()

dt = ng()

out_dir = f"{cwd}/out"
out_dir_dt = f"{cwd}/out/{dt}"

with open(f'{cwd}/log/{dt}/result.json') as f:
    data = json.load(f)

run(f"mkdir -p {out_dir_dt}")
os.chdir(out_dir_dt)

with open("index.html", 'w') as f:
    f.write(f"{data['used_time']}")

os.chdir(out_dir)
run(f"scp -r -C {dt} uwplse.org:/var/www/zombie/")
url = f"http://zombie.uwplse.org/{dt}"
run(f"""nightly-results url {url} || true""")
