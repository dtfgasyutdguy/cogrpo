# -*- coding: utf-8 -*-
from typing import Set



AVOIDED_APPS:Set[str]=set([
    'AgentUI'
# BROWSER_NAMES=set([
#     'msedge.exe',
#     'chrome.exe',
#     'firefox.exe'
# ])
])

EXCLUDED_APPS:Set[str]=set([
    'Progman',
    'Shell_TrayWnd',
    'Shell_SecondaryTrayWnd',
    'Microsoft.UI.Content.PopupWindowSiteBridge',
    'Windows.UI.Core.CoreWindow',
])

PROCESS_PER_MONITOR_DPI_AWARE = 2