# -*- coding: utf-8 -*-
import logging

# ...existing code...


    """Start the web server"""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    logger = logging.getLogger(__name__)
    
    # ...existing code...
    
    # Change this line:
# def start_server(host='0.0.0.0', port=9876, debug=False):
    # logger.info(f"Web interface available at http://{host}:{port}")
    
    # To this (more discreet version):
    logger.info(f"Server started on port {port}")
    
    # ...existing code...

# ...existing code...