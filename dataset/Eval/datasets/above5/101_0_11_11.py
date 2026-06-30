# -*- coding: utf-8 -*-
import sys
from pypdf import PdfReader

# if (reader.get_fields()):

# Script for Claude to run to determine whether a PDF has fillable form fields. See forms.md.


reader = PdfReader(sys.argv[1])

    print("This PDF has fillable form fields")
else:
    print("This PDF does not have fillable form fields; you will need to visually determine where to enter data")
