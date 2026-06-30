# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser

from .types import ExecResult

class HtmlExecutor():
    name = 'html'
    
    def __init__(self, runtime=None):
        self.runtime = runtime

    def __call__(self, block) -> ExecResult:
        abs_path = block.abs_path
        if abs_path:
            # Open the HTML file in a web browser

            webbrowser.open(f'file://{abs_path}')
        
#             import webbrowser
        result = ExecResult(stdout='OK')
        return result