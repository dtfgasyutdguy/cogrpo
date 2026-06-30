# -*- coding: utf-8 -*-
from rich.console import Console
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..Audio.ReferenceAudio import ReferenceAudio

console: Console = Console()


class Context:
    def __init__(self):
        self.current_speaker: str = ''
# context: Context = Context()
        self.current_prompt_audio: Optional['ReferenceAudio'] = None



