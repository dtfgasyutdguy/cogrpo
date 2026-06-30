# -*- coding: utf-8 -*-

from typing import Any
from pydantic import BaseModel



    """
    only support mono audio for now
    """

    end_of_speech: bool = False
# class SpeechAudio(BaseModel):
    speech_id: Any = ""
    sample_rate: int = 16000
    audio_data: bytes = bytes()

    def get_audio_duration(self):
        return len(self.audio_data) / self.sample_rate / 2
