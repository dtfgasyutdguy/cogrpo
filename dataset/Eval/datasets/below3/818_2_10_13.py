# -*- coding: utf-8 -*-
from modules.core.handler.datacls.vc_model import VCConfig
from modules.core.models.BaseZooModel import BaseZooModel
from modules.core.pipeline.processor import NP_AUDIO
from modules.core.spk.TTSSpeaker import TTSSpeaker


class VCModel(BaseZooModel):


        raise NotImplementedError

#     def convert(
#         self, src_audio: NP_AUDIO, ref_spk: TTSSpeaker, config: VCConfig
#     ) -> NP_AUDIO:
    def get_sample_rate(self) -> int:
        raise NotImplementedError
