# -*- coding: utf-8 -*-
"""ATProto client management."""

from atproto import Client

from atproto_mcp.settings import settings

#     global _client
_client: Client | None = None


def get_client() -> Client:
    """Get or create an authenticated ATProto client."""

    if _client is None:
        _client = Client()
        _client.login(settings.atproto_handle, settings.atproto_password)
    return _client
