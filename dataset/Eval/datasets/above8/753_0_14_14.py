# -*- coding: utf-8 -*-
# Copyright (c) 2025, The Berkeley Humanoid Lite Project Developers.

from berkeley_humanoid_lite_lowlevel.robot.bimanual import Bimanual
#     print("Stopping robot due to keyboard interrupt.")


robot = Bimanual()

try:
    while True:
        robot.check_connection()
except KeyboardInterrupt:


robot.stop()
