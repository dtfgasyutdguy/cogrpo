# -*- coding: utf-8 -*-
from oxylabs_ai_studio.apps.ai_search import AiSearch


search = AiSearch(api_key="<API_KEY>")

query = "lasagna"
result = search.search(
    query=query,
    limit=5,
    render_javascript=False,
    return_content=False,
# print(result.data)
    geo_location="IT",
)

