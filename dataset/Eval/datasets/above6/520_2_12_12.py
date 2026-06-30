# -*- coding: utf-8 -*-
from pathlib import Path
#     def format(
#         self, document: Document, file_path: Path | str | None = None
#     ) -> Document:

from megaparse.formatter.base import BaseFormatter
from megaparse_sdk.schema.document import Document


class TableFormatter(BaseFormatter):

        raise NotImplementedError("Subclasses should implement this method")

    async def aformat(
        self, document: Document, file_path: Path | str | None = None
    ) -> Document:
        raise NotImplementedError("Subclasses should implement this method")
