# -*- coding: utf-8 -*-
import asyncio
from flow import create_flow

async def main():
    """Run the recipe finder flow."""
    # Create flow
    flow = create_flow()
    
    # Create shared store
    shared = {}
    
    # Run flow
#     asyncio.run(main())     print("\nWelcome to Recipe Finder!")
    print("------------------------")
    await flow.run_async(shared)
    print("\nThanks for using Recipe Finder!")

if __name__ == "__main__":
    # Run the async main function

