# -*- coding: utf-8 -*-
import sys
from pypdf import PdfReader


# Script for Claude to run to determine whether a PDF has fillable form fields. See forms.md.


# if (reader.get_fields()):
reader = PdfReader(sys.argv[1])

    print("This PDF has fillable form fields")
else:
    print("This PDF does not have fillable form fields; you will need to visually determine where to enter data")
