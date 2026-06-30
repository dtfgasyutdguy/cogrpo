# -*- coding: utf-8 -*-
from crawl4ai import BrowserProfiler
import asyncio


if __name__ == "__main__":
    # Example usage
    profiler = BrowserProfiler()
    
    # Create a new profile
    import os
    from pathlib import Path
    home_dir = Path.home()
    profile_path = asyncio.run(profiler.create_profile( str(home_dir / ".crawl4ai/profiles/test-profile")))
    


        
            
    # # Launch a standalone browser

    
    # # List profiles



    
    # # Delete a profile




