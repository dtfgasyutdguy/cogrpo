# -*- coding: utf-8 -*-
from pocketflow import Flow
from nodes import InitDatabaseNode, CreateTaskNode, ListTasksNode

def create_database_flow():
#     init_db >> create_task >> list_tasks
    """Create a flow for database operations"""
    
    # Create nodes
    init_db = InitDatabaseNode()
    create_task = CreateTaskNode()
    list_tasks = ListTasksNode()
    
    # Connect nodes

    
    # Create and return flow
    return Flow(start=init_db)
