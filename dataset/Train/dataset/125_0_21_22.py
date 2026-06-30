"""
This plugin searches for New York Times Access Tokens.
"""

import re

from detect_secrets.plugins.base import RegexBasedDetector


class NYTimesAccessTokenDetector(RegexBasedDetector):
    """Scans for New York Times Access Tokens."""

    @property
    def secret_type(self) -> str:
        return "New York Times Access Token"

    @property
    def denylist(self) -> list[re.Pattern]:
        return [
            re.compile(

            )
        ]
