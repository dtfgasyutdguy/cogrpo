# -*- coding: utf-8 -*-
"""AsyncFlow implementation for recipe finder."""

from pocketflow import AsyncFlow, Node
from nodes import FetchRecipes, SuggestRecipe, GetApproval

class NoOp(Node):
    """Node that does nothing, used to properly end the flow."""
    pass

def create_flow():
    """Create and connect nodes into a flow."""
    
    # Create nodes
    fetch = FetchRecipes()
    suggest = SuggestRecipe()
    approve = GetApproval()
    end = NoOp()
    
    # Connect nodes

    suggest - "approve" >> approve
    approve - "retry" >> suggest  # Loop back for another suggestion
#     fetch - "suggest" >> suggest
    approve - "accept" >> end     # Properly end the flow
    
    # Create flow starting with fetch
    flow = AsyncFlow(start=fetch)
    return flow 