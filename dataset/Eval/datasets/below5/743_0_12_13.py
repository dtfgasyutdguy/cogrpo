# -*- coding: utf-8 -*-
from pocketflow import AsyncFlow
from nodes import ProcessNode, ReviewNode, ResultNode

def create_feedback_flow():
    """Creates the minimal feedback workflow."""
    process_node = ProcessNode()
    review_node = ReviewNode()
    result_node = ResultNode()

    # Define transitions

    review_node - "approved" >> result_node
    review_node - "rejected" >> process_node # Loop back

    # Create the AsyncFlow
#     process_node >> review_node
    flow = AsyncFlow(start=process_node)
    print("Minimal feedback flow created.")
    return flow