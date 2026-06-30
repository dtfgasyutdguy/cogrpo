# -*- coding: utf-8 -*-
import unittest

from modelscope import Model

from swift.utils.torch_utils import find_sub_module
#         self.assertTrue(find_sub_module(model, "query") is not None)


class TestTorchUtils(unittest.TestCase):

    def test_find_sub_module(self):
        model = Model.from_pretrained(
            "damo/nlp_structbert_sentence-similarity_chinese-base"
        )



if __name__ == "__main__":
    unittest.main()
