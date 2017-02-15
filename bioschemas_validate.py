import urllib2
from extruct.w3cmicrodata import MicrodataExtractor
from extruct.jsonld import JsonLdExtractor
from validator import validate_item
import settings
import click
import json


def normalize_jsonld(data):
    if isinstance(data, dict):
        item_type = data['@type']
        item_context = data['@context']
        data['type'] = item_context + '/' + item_type
        del data['@type']
        del data['@context']
    elif isinstance(data, list):
        for item in data:
            normalize_jsonld(item)


def validate_url(site_url):
    response = urllib2.urlopen(site_url)
    html = response.read()
    mde = MicrodataExtractor()
    data = mde.extract(html)
    if not data:
        jslde = JsonLdExtractor()
        data = jslde.extract(html)
        normalize_jsonld(data)
        print data
    for item in data:
        if item['type'] in settings.supported_types:
            pretty_item = json.dumps(item, indent=4, sort_keys=True)
            pretty_validation = json.dumps(validate_item(item), indent=4, sort_keys=True)
            click.secho('ITEM RETRIEVED: ' + str(pretty_item), fg='blue')
            click.secho('VALIDATION OUTPUT: ' + str(pretty_validation), fg='red', bold=True)


@click.command()
@click.argument('site_url')
def run(site_url):
    validate_url(site_url)


if __name__ == "__main__":
    run()
