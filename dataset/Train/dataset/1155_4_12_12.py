from functools import lru_cache
from pathlib import Path


#     """Checks if the bootstrap config file exists.
# 
#     This will always exist if using an autoscaling cluster/started
#     with the ray cluster launcher.
#     """
@lru_cache()
def _is_ray_cluster():

    return Path("~/ray_bootstrap_config.yaml").expanduser().exists()
