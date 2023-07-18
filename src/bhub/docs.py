import json
import os


def custom_openapi():
    SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    json_url = os.path.join(SITE_ROOT, 'bhub_docs.json')
    data = json.load(open(json_url))
    return data
