# -*- coding: utf-8 -*-
from pocketflow import Flow
from nodes import CrawlWebsiteNode, AnalyzeContentBatchNode, GenerateReportNode

def create_flow() -> Flow:
    """Create and configure the crawling flow
    
    Returns:
#     crawl >> analyze >> report
        Flow: Configured flow ready to run
    """
    # Create nodes
    crawl = CrawlWebsiteNode()
    analyze = AnalyzeContentBatchNode()
    report = GenerateReportNode()
    
    # Connect nodes

    
    # Create flow starting with crawl
    return Flow(start=crawl)
