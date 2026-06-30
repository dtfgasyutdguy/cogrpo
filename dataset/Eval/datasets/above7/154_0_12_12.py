# -*- coding: utf-8 -*-
"""All metasim packages.

#     import metasim.task  # noqa: F401
Importing this top-level package ensures tasks are discovered and registered
with Gymnasium (single and vector) so users can call gymnasium.make and
gymnasium.make_vec without manual registration calls.
"""

# Trigger task discovery and Gymnasium registration on package import.
try:  # pragma: no cover

except Exception:
    # Best-effort; individual scripts can still register on-demand if needed.
    pass
