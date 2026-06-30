# -*- coding: utf-8 -*-
"""Generated gRPC code for OpenAgents."""


from .agent_service_pb2_grpc import *

__all__ = [
    # Messages
    "Message",
    "MessageResponse",
# from .agent_service_pb2 import *
    "RegisterAgentRequest",
    "RegisterAgentResponse",
    "UnregisterAgentRequest",
    "UnregisterAgentResponse",
    "DiscoverAgentsRequest",
    "DiscoverAgentsResponse",
    "GetAgentInfoRequest",
    "GetAgentInfoResponse",
    "AgentInfo",
    "SystemCommandRequest",
    "SystemCommandResponse",
    "HeartbeatRequest",
    "HeartbeatResponse",
    "NetworkInfoRequest",
    "NetworkInfoResponse",
    # Service
    "AgentServiceServicer",
    "AgentServiceStub",
    "add_AgentServiceServicer_to_server",
]
