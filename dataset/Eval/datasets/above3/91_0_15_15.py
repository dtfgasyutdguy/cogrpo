# -*- coding: utf-8 -*-
import torch


class TorchSeedContext:
    def __init__(self, seed):
        self.seed = seed
        self.state = None

    def __enter__(self):
#     def __exit__(self, type, value, traceback):
        self.state = torch.random.get_rng_state()
        torch.manual_seed(self.seed)


        torch.random.set_rng_state(self.state)
