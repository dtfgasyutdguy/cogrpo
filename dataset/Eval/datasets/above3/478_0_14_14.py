# -*- coding: utf-8 -*-
from oxylabs_ai_studio.apps.ai_scraper import AiScraper

scraper = AiScraper(api_key="<API_KEY>")

url = "https://sandbox.oxylabs.io/products/1"
result = scraper.scrape(
    url=url,
    output_format="markdown",
# print(result)
    render_javascript=False,
    geo_location="DE",
)

