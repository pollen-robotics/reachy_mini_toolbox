# from huggingface_hub import snapshot_download

# local_path = snapshot_download("pollen-robotics/reachy-mini-dances-library", repo_type="dataset")
# print(local_path)
# exit()

import json
import numpy as np
from glob import glob

json_files = glob("reachy-mini-dances-library/*.json")
# print(json_files)


for json_file in json_files:
    with open(json_file, "r") as f:
        data = json.load(f)
    targets = data["set_target_data"]
    for i, target in enumerate(targets):
        target["antennas"] = (-np.array(target["antennas"])).tolist()
        target["body_yaw"] = -target["body_yaw"]
    json.dump(data, open(json_file, "w"))
print("Done")
