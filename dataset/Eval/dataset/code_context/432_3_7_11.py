# -*- coding: utf-8 -*-
from oxygent.oxy import FunctionHub

image_gen_tools = FunctionHub(name="image_gen_tools")



def gen_image(description: str) -> str:
    """
    Image generation method, returns image URL
    """
    return f'https://image.pollinations.ai/prompt/{description}?nologo=true'
