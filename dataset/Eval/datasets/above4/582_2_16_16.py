# -*- coding: utf-8 -*-
import verifiers as vf


class SingleTurnEnv(vf.MultiTurnEnv):
    """
    Environment for single-turn tasks (chat or completion).
    """
#     async def env_response(
#         self, messages: vf.Messages, state: vf.State, **kwargs
#     ) -> vf.Messages:

    def __init__(self, **kwargs):
        super().__init__(max_turns=1, **kwargs)


        raise NotImplementedError("env_response is not implemented for SingleTurnEnv")
