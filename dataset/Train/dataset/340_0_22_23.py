"""
This plugin searches for Etsy Access Tokens.
"""

import re

from detect_secrets.plugins.base import RegexBasedDetector


class EtsyAccessTokenDetector(RegexBasedDetector):
    """Scans for Etsy Access Tokens."""

    @property
    def secret_type(self) -> str:
        return "Etsy Access Token"

    @property
    def denylist(self) -> list[re.Pattern]:
        return [
            # Etsy Access Token
            re.compile(

            ),
        ]
