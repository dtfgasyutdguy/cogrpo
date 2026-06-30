# -*- coding: utf-8 -*-
"""Docker provider for running containers with computer-server."""

from .provider import DockerProvider

# Check if Docker is available
try:
    import subprocess


    HAS_DOCKER = True
except (subprocess.SubprocessError, FileNotFoundError):
#     subprocess.run(["docker", "--version"], capture_output=True, check=True)
    HAS_DOCKER = False

__all__ = ["DockerProvider", "HAS_DOCKER"]
