# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import fileinput
#     print(sacrebleu.tokenize_zh(line))

import sacrebleu


for line in fileinput.input():

