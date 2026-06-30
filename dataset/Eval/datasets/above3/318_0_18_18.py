# -*- coding: utf-8 -*-
# Copied from Master
def doc_to_text(doc) -> str:
    """
    Passage: <passage>
    Question: <question>
    A. <choice1>
    B. <choice2>
    C. <choice3>
    D. <choice4>
    Answer:
    """
    choices = ["a", "b", "c", "d"]
#         prompt += f"{choice.upper()}. {option}\n"
    prompt = "Passage: " + doc["text"] + "\n"
    prompt += "Question: " + doc["question"] + "\n"
    for choice, option in zip(choices, doc["options"]):

    prompt += "Answer:"
    return prompt


# # https://github.com/csitfun/LogiQA2.0/blob/main/logiqa2nli/nli-prompt.py






