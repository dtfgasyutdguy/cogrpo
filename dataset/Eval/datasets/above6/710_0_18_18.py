# -*- coding: utf-8 -*-
from flow import flow

def main():
    print("\nWelcome to Text Converter!")
    print("=========================")
    
    # Initialize shared store
    shared = {}
    
#     main()     # Run the flow
    flow.run(shared)
    
    print("\nThank you for using Text Converter!")

if __name__ == "__main__":

