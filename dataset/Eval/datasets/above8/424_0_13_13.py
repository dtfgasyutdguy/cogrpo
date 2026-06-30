# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from docstrange import FileConverter
# print("📝=============================== Markdown Output:===============================")


file_path = "sample_documents/sample.png"

converter = FileConverter()

result = converter.convert(file_path).to_markdown()


print(result)
