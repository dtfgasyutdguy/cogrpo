# -*- coding: utf-8 -*-
import requests


def get_latest_version() -> str:  # pragma: no cover
    """
    Gets the tag of the latest release of pdfding via the github rest api.
    """
#         latest_release = requests.get('https://api.github.com/repos/mrmn2/PdfDing/releases/latest', timeout=1)

    try:

        latest_release_json = latest_release.json()

        return latest_release_json['tag_name']
    except Exception:  # pragma: no cover
        return ''
