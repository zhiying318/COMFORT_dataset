# comfort_human_car_pov_config.py
# Same scene setup as comfort_human_car, but adds 4 first-person POV cameras
# placed at person's eye level (height=1.5), facing 4 directions.
# For POV cameras, addressee=False to hide the human model (first-person view).

from data_generation.constants import *
from data_generation.comfort_human_car_config import (
    COMFORT_HUMAN_CAR_DEFAULT_CONFIG,
    COMFORT_HUMAN_CAR_OBJECTS,
    COMFORT_HUMAN_CAR_RELATIONS,
    ALL_CAMERAS as EXTERNAL_CAMERAS,
)

POV_HEIGHT = 1.5  # approximate eye height in world units
# Look toward the ground point at CARDINAL_DISTANCE (same distance as where objects are placed).
# Downward angle: atan(1.5 / 2.5) ≈ 31° — objects appear near centre of frame.
from data_generation.comfort_human_car_config import CARDINAL_DISTANCE
POV_LOOK_DISTANCE = CARDINAL_DISTANCE  # 2.5 units
POV_LOOK_HEIGHT = 0.0
POV_LENS_MM = 24.0  # wide-angle focal length for POV cameras (default Blender = 50mm)

# Person faces toward -Y (cam_front side shows face, yaw=270 in config)
CAMERA_POV_FRONT = {
    "view_name": "cam_pov_front",
    "cam_position": (0.0, 0.0, POV_HEIGHT),
    "cam_look_at": (0.0, -POV_LOOK_DISTANCE, POV_LOOK_HEIGHT),
    "cam_lens": POV_LENS_MM,
    "addressee": False,  # hide human for first-person view
}

CAMERA_POV_BACK = {
    "view_name": "cam_pov_back",
    "cam_position": (0.0, 0.0, POV_HEIGHT),
    "cam_look_at": (0.0, POV_LOOK_DISTANCE, POV_LOOK_HEIGHT),
    "cam_lens": POV_LENS_MM,
    "addressee": False,
}

CAMERA_POV_LEFT = {
    "view_name": "cam_pov_left",
    "cam_position": (0.0, 0.0, POV_HEIGHT),
    "cam_look_at": (POV_LOOK_DISTANCE, 0.0, POV_LOOK_HEIGHT),
    "cam_lens": POV_LENS_MM,
    "addressee": False,
}

CAMERA_POV_RIGHT = {
    "view_name": "cam_pov_right",
    "cam_position": (0.0, 0.0, POV_HEIGHT),
    "cam_look_at": (-POV_LOOK_DISTANCE, 0.0, POV_LOOK_HEIGHT),
    "cam_lens": POV_LENS_MM,
    "addressee": False,
}

POV_CAMERAS = [
    CAMERA_POV_FRONT,
    CAMERA_POV_BACK,
    CAMERA_POV_LEFT,
    CAMERA_POV_RIGHT,
]

ALL_CAMERAS_POV = EXTERNAL_CAMERAS + POV_CAMERAS

COMFORT_HUMAN_CAR_POV_DEFAULT_CONFIG = COMFORT_HUMAN_CAR_DEFAULT_CONFIG
COMFORT_HUMAN_CAR_POV_OBJECTS = COMFORT_HUMAN_CAR_OBJECTS
COMFORT_HUMAN_CAR_POV_RELATIONS = COMFORT_HUMAN_CAR_RELATIONS
