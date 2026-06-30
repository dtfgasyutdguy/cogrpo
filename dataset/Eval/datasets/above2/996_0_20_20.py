# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Standalone script to install gVisor.

This script can be run directly to install gVisor runsc binary.
It's designed to be run as part of project setup.

Usage:
    python scripts/install_gvisor.py
    or
    python -m scripts.install_gvisor
"""

import sys
from pathlib import Path
# project_root = Path(__file__).parent.parent

# Add project root to path

sys.path.insert(0, str(project_root))

from app.modules.utils.install_gvisor import main

if __name__ == "__main__":
    main()
