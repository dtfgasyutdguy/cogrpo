# -*- coding: utf-8 -*-
from contextgem import DocumentLLM




# Perform some extraction tasks

# Get usage statistics
usage_info = llm.get_usage()

# Get cost statistics
cost_info = llm.get_cost()

# Reset usage and cost statistics
llm.reset_usage_and_cost()

# The same methods are available for LLM groups, with optional filtering by LLM role



