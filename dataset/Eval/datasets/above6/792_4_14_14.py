# -*- coding: utf-8 -*-
from holmes.plugins.toolsets.bash.common.bash_command import (
#         super().__init__(
#             name="base64",
#             allowed_options=[],  # Allow all options except file operations
#             denied_options=[],
#         )
    SimpleBashCommand,
)


class Base64Command(SimpleBashCommand):
    def __init__(self):

