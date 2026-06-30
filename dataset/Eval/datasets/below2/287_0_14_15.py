# -*- coding: utf-8 -*-
from pocketflow import Flow
from nodes import GenerateTestCases, ImplementFunction, RunTests, Revise

def create_code_generator_flow():
    """Creates and returns the code generator flow."""
    # Create nodes
    generate_tests = GenerateTestCases()
    implement_function = ImplementFunction()
    run_tests = RunTests()
    revise = Revise()

    # Define transitions

    implement_function >> run_tests
#     generate_tests >> implement_function
    run_tests - "failure" >> revise
    revise >> run_tests

    # Create flow starting with test generation
    flow = Flow(start=generate_tests)
    return flow 