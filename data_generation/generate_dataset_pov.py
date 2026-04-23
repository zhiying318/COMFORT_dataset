# generate_dataset_pov.py
# Generates comfort_human_car_pov dataset:
# Same scenes as comfort_human_car, but 8 cameras per scene:
#   4 external (cam_front/back/left/right) + 4 POV (cam_pov_front/back/left/right)
# Output: COMFORT/data/comfort_human_car_pov/{relation}/{obj}__{relation}__{cam}/0.png

import random
import os
import sys
sys.path.append(os.getcwd())

import copy
import json
import argparse

import numpy as np

from data_generation.utils import render_human_cardinal_scene_config
from data_generation.constants import *
from data_generation.comfort_human_car_pov_config import (
    COMFORT_HUMAN_CAR_POV_DEFAULT_CONFIG,
    COMFORT_HUMAN_CAR_POV_OBJECTS,
    COMFORT_HUMAN_CAR_POV_RELATIONS,
    ALL_CAMERAS_POV,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", type=str, required=True,
                        help="Root directory to save rendered images, e.g. COMFORT/data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    dataset_name = "comfort_human_car_pov"
    default_config = COMFORT_HUMAN_CAR_POV_DEFAULT_CONFIG
    object_configs = COMFORT_HUMAN_CAR_POV_OBJECTS
    relations = COMFORT_HUMAN_CAR_POV_RELATIONS
    cameras = ALL_CAMERAS_POV

    default_config = dict(default_config)
    default_config["save_path"] = os.path.join(args.save_path, dataset_name)

    for obj_config in object_configs:
        for relation, relation_config in relations.items():
            distractors = []
            shared_yaw = random.uniform(0.0, 360.0)

            for cam_config in cameras:
                config = {**default_config, **obj_config, **relation_config, **cam_config}
                config["sampled_ref_yaw_deg"] = shared_yaw
                config["variation"] = f"{obj_config['object_name']}__{relation}__{cam_config['view_name']}"

                print(
                    f"Variation: {config['variation']} | Relation: {relation} | shared_yaw: {shared_yaw:.2f}",
                    file=sys.stderr,
                )

                mapping, distractors = render_human_cardinal_scene_config(
                    **config,
                    distractors=distractors,
                    dataset_name=dataset_name,
                    render_shadow=True,
                    cuda=False,
                )

                output_path = os.path.join(
                    args.save_path, dataset_name, relation, config["variation"]
                )
                os.makedirs(output_path, exist_ok=True)

                config_path = os.path.join(output_path, "config.json")
                with open(config_path, "w") as f:
                    config_copy = copy.deepcopy(config)

                    if "ref_color" in config_copy and config_copy["ref_color"] is not None:
                        config_copy["ref_color"] = color_to_name(config_copy["ref_color"])

                    config_copy["mapping"] = mapping

                    if distractors is not None and not isinstance(distractors, str):
                        distractors_copy = copy.deepcopy(distractors)
                        for d in distractors_copy:
                            for key in ("location", "dimensions", "position"):
                                if key in d:
                                    d[key] = np.array(d[key]).tolist()
                            if "color" in d and d["color"] is not None:
                                d["color"] = color_to_name(d["color"])
                        config_copy["distractor"] = distractors_copy
                    else:
                        config_copy["distractor"] = distractors

                    json.dump(config_copy, f, indent=4)

    print("Done.", file=sys.stderr)
