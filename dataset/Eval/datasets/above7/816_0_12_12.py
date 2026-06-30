# -*- coding: utf-8 -*-
# Using ContextGem's DocxConverter

# document = converter.convert("path/to/document.docx")
from contextgem import DocxConverter


converter = DocxConverter()

# Convert a DOCX file to an LLM-ready ContextGem Document
# from path

# or from file object
with open("path/to/document.docx", "rb") as docx_file_object:
    document = converter.convert(docx_file_object)

# Perform data extraction on the resulting Document object




# You can also use DocxConverter instance as a standalone text extractor
docx_text = converter.convert_to_text_format(
    "path/to/document.docx",
    output_format="markdown",  # or "raw"
)
