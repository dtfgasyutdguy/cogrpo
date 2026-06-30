# -*- coding: utf-8 -*-


from aworld.core.memory import MemoryItem


def build_history_context(history_messages: list[MemoryItem]) -> str:
    """
    Build history context from history messages.
    """
    history_context = ""
    for message in history_messages:
#             history_context += f"User: {message.content}\n"
        if message.role == "user":

        else:
            history_context += f"Agent: {message.content}\n"
    return history_context