# generate_dataset_pov_two.py
# Generates comfort_human_car_pov_two dataset:
#   Same 8 cameras as comfort_human_car_pov, but each scene contains TWO objects:
#   - ref_object at its cardinal position (determines the correct POV answer)
#   - third_object at one of the 3 remaining cardinal positions (adds visual complexity)
#
# Dataset size: 9 ref_objects × 4 relations × 3 third_object positions × 8 cameras = 864 images
#
# Run from /home/zzou/COMFORT/:
#   python data_generation/generate_dataset_pov_two.py --save_path ../COMFORT/data

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
from data_generation.comfort_human_car_pov_two_config import (
    COMFORT_HUMAN_CAR_POV_TWO_DEFAULT_CONFIG,
    COMFORT_HUMAN_CAR_POV_TWO_OBJECTS,
    COMFORT_HUMAN_CAR_POV_TWO_RELATIONS,
    ALL_CAMERAS_POV_TWO,
    CARDINAL_OFFSETS,
    REMAINING_POSITIONS,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", type=str, required=True,
                        help="Root directory to save rendered images, e.g. COMFORT/data")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)

    dataset_name = "comfort_human_car_pov_two"
    default_config = dict(COMFORT_HUMAN_CAR_POV_TWO_DEFAULT_CONFIG)
    default_config["save_path"] = os.path.join(args.save_path, dataset_name)

    object_configs  = COMFORT_HUMAN_CAR_POV_TWO_OBJECTS
    relations       = COMFORT_HUMAN_CAR_POV_TWO_RELATIONS
    cameras         = ALL_CAMERAS_POV_TWO

    for ref_obj_config in object_configs:
        ref_name = ref_obj_config["object_name"]

        # Pool of other objects to choose from as third_object
        other_objects = [o for o in object_configs if o["object_name"] != ref_name]

        for relation, relation_config in relations.items():
            remaining_positions = REMAINING_POSITIONS[relation]

            for third_pos in remaining_positions:
                # Pick a random third object (different from ref_object)
                third_obj_config = random.choice(other_objects)
                third_name = third_obj_config["object_name"]

                shared_yaw_ref   = random.uniform(0.0, 360.0)
                shared_yaw_third = random.uniform(0.0, 360.0)

                distractors = []

                for cam_config in cameras:
                    config = {
                        **default_config,
                        **ref_obj_config,
                        **relation_config,
                        **cam_config,
                    }
                    config["sampled_ref_yaw_deg"] = shared_yaw_ref

                    # third_object parameters (prefix third_obj_*)
                    config["third_obj_shape"]           = third_obj_config["ref_shape"]
                    config["third_obj_color"]           = third_obj_config.get("ref_color", None) or None
                    config["third_obj_size"]            = third_obj_config["ref_size"]
                    config["third_obj_position"]        = third_obj_config["ref_position"]
                    config["third_obj_rotation"]        = third_obj_config["ref_rotation"]
                    config["third_obj_cardinal_offset"] = CARDINAL_OFFSETS[third_pos]
                    config["third_obj_yaw_deg"]         = shared_yaw_third

                    variation_name = (
                        f"{ref_name}__{relation}__{cam_config['view_name']}"
                        f"__third_{third_name}_at_{third_pos}"
                    )
                    config["variation"] = variation_name

                    print(
                        f"Variation: {variation_name} | ref_yaw={shared_yaw_ref:.1f} | third_yaw={shared_yaw_third:.1f}",
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
                        args.save_path, dataset_name, relation, variation_name
                    )
                    os.makedirs(output_path, exist_ok=True)

                    config_path = os.path.join(output_path, "config.json")
                    config_save = copy.deepcopy(config)

                    if "ref_color" in config_save and config_save["ref_color"] is not None:
                        config_save["ref_color"] = color_to_name(config_save["ref_color"])
                    if "third_obj_color" in config_save and config_save["third_obj_color"] is not None:
                        config_save["third_obj_color"] = color_to_name(config_save["third_obj_color"])

                    config_save["mapping"]       = mapping
                    config_save["distractor"]    = []
                    config_save["third_obj_name"] = third_name
                    config_save["third_obj_position_relation"] = third_pos

                    # convert tuples to lists for JSON serialisation
                    for key, val in config_save.items():
                        if isinstance(val, (tuple, np.ndarray)):
                            config_save[key] = list(val)

                    with open(config_path, "w") as f:
                        json.dump(config_save, f, indent=4)

    print("Done.", file=sys.stderr)
