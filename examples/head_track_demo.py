"""Head tracking demo for Reachy Mini."""

import time

import cv2
import numpy as np
from reachy_mini import ReachyMini
from reachy_mini.utils.camera import find_camera

# from head_tracker import HeadTracker
from scipy.spatial.transform import Rotation as R

from reachy_mini_toolbox.vision import HeadTracker


def draw_debug(img, eye_center, roll):
    """Draw debug information on the image."""
    _eye_center = (eye_center.copy() + 1) / 2  # [0, 1]
    h, w, _ = img.shape
    cv2.circle(
        img,
        (int(_eye_center[0] * w), int(_eye_center[1] * h)),
        radius=5,
        color=(0, 0, 255),
        thickness=-1,
    )

    _target = [0.5, 0.5]
    cv2.circle(
        img,
        (int(_target[0] * w), int(_target[1] * h)),
        radius=5,
        color=(255, 0, 0),
        thickness=-1,
    )

    cv2.line(
        img,
        (int(_eye_center[0] * w), int(_eye_center[1] * h)),
        (int(_target[0] * w), int(_target[1] * h)),
        color=(0, 255, 0),
        thickness=2,
    )
    cv2.line(
        img,
        (int(_eye_center[0] * w), int(_eye_center[1] * h)),
        (
            int(_eye_center[0] * w + 100 * np.cos(roll)),
            int(_eye_center[1] * h + 100 * np.sin(roll)),
        ),
        color=(255, 255, 0),
        thickness=2,
    )


cap = find_camera()

head_tracker = HeadTracker()
pose = np.eye(4)
euler_rot = np.array([0.0, 0.0, 0.0])
kp = 0.3
t0 = time.time()
with ReachyMini() as reachy_mini:
    try:
        while True:
            t = time.time() - t0

            success, img = cap.read()

            eye_center, roll = head_tracker.get_head_position(img)
            if eye_center is not None:
                draw_debug(img, eye_center, roll)

                target = [0, 0]
                error = np.array(target) - eye_center  # [-1, 1] [-1, 1]
                euler_rot += np.array(
                    [kp * roll * 0.1, -kp * 0.1 * error[1], kp * error[0]]
                )

                rot_mat = R.from_euler("xyz", euler_rot, degrees=False).as_matrix()
                pose[:3, :3] = rot_mat
                pose[:3, 3][2] = (
                    error[1] * 0.04
                )  # Adjust height based on vertical error

                reachy_mini.set_target(head=pose)
            cv2.imshow("test_window", img)

            cv2.waitKey(1)
    except KeyboardInterrupt:
        pass
