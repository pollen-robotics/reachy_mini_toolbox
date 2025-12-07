"""Reachy Mini Look At Head Tracking Example.

Uses the lookat() api to have Reachy Mini follow the user's head movements.
"""

import cv2
from reachy_mini import ReachyMini

from reachy_mini_toolbox.vision import HeadTracker

head_tracker = HeadTracker()

with ReachyMini() as reachy_mini:
    try:
        while True:
            img = reachy_mini.media.get_frame()
            if img is not None:
                eye_center, roll = head_tracker.get_head_position(img)
                if eye_center is not None:
                    h, w, _ = img.shape
                    eye_center = (eye_center + 1) / 2
                    eye_center[0] *= w
                    eye_center[1] *= h
                    cv2.circle(
                        img,
                        center=(int(eye_center[0]), int(eye_center[1])),
                        radius=5,
                        color=(0, 255, 0),
                        thickness=2,
                    )
                    reachy_mini.look_at_image(*eye_center, duration=0.0)

            cv2.imshow("image", img)

            cv2.waitKey(1)
    except KeyboardInterrupt:
        pass
