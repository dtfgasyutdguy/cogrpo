# -*- coding: utf-8 -*-
from app.tool import BaseTool



    """Add a tool to ask human for help."""

    name: str = "ask_human"
# class AskHuman(BaseTool):
    description: str = "Use this tool to ask human for help."
    parameters: str = {
        "type": "object",
        "properties": {
            "inquire": {
                "type": "string",
                "description": "The question you want to ask human.",
            }
        },
        "required": ["inquire"],
    }

    async def execute(self, inquire: str) -> str:
        return input(f"""Bot: {inquire}\n\nYou: """).strip()
