# comfort_human_car_pov_two_config.py
# Extends test02 (pov) config: same 8 cameras, but adds a third_object
# placed at one of the 3 remaining cardinal positions (the 3 not occupied by ref_object).
# Generates 3 dataset variants per (ref_object, relation) scene.

from data_generation.constants import *
from data_generation.comfort_human_car_config import (
    COMFORT_HUMAN_CAR_DEFAULT_CONFIG,
    COMFORT_HUMAN_CAR_OBJECTS,
    COMFORT_HUMAN_CAR_RELATIONS,
    CARDINAL_DISTANCE,
)
from data_generation.comfort_human_car_pov_config import ALL_CAMERAS_POV

# All 4 cardinal offsets, keyed by relation string
CARDINAL_OFFSETS = {
    FRONT:  (0.0, -CARDINAL_DISTANCE, 0.0),   # "infrontof"
    BEHIND: (0.0,  CARDINAL_DISTANCE, 0.0),   # "behind"
    LEFT:   ( CARDINAL_DISTANCE, 0.0, 0.0),   # "totheleft"
    RIGHT:  (-CARDINAL_DISTANCE, 0.0, 0.0),   # "totheright"
}

# For each relation, the 3 remaining positions for the third_object
REMAINING_POSITIONS = {
    FRONT:  [BEHIND, LEFT,  RIGHT],
    BEHIND: [FRONT,  LEFT,  RIGHT],
    LEFT:   [FRONT,  BEHIND, RIGHT],
    RIGHT:  [FRONT,  BEHIND, LEFT],
}

COMFORT_HUMAN_CAR_POV_TWO_DEFAULT_CONFIG = COMFORT_HUMAN_CAR_DEFAULT_CONFIG
COMFORT_HUMAN_CAR_POV_TWO_OBJECTS       = COMFORT_HUMAN_CAR_OBJECTS
COMFORT_HUMAN_CAR_POV_TWO_RELATIONS     = COMFORT_HUMAN_CAR_RELATIONS
ALL_CAMERAS_POV_TWO                     = ALL_CAMERAS_POV
