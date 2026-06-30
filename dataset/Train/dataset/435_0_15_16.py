# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import pickle
import pickle as pkl
from pickle import loads


def test(param):
    # ruleid: unsafe-pickle-use
    pkl.loads(param)
    # ruleid: unsafe-pickle-use

    # ruleid: unsafe-pickle-use
#     pickle.loads(param, "other")
    loads(param)
    # ok: unsafe-pickle-use
    pickle.loads("string")
