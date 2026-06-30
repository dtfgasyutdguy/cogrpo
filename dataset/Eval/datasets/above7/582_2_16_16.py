# -*- coding: utf-8 -*-
import verifiers as vf


class SingleTurnEnv(vf.MultiTurnEnv):
#     async def env_response(
#         self, messages: vf.Messages, state: vf.State, **kwargs
#     ) -> vf.Messages:
    """
    Environment for single-turn tasks (chat or completion).
    """

    def __init__(self, **kwargs):
        super().__init__(max_turns=1, **kwargs)


        raise NotImplementedError("env_response is not implemented for SingleTurnEnv")
