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
            validation = validate_item(item)
            click.secho('ITEM RETRIEVED', fg='blue', bold=True)
            click.secho(str(pretty_item), fg='blue')
            click.secho('VALIDATION FULL REPORT', fg='green', bold=True)
            for line in validation['full_report'].split('\n'):
                if 'ERROR' in line:
                    color = 'red'
                else:
                    color = 'yellow'
                click.secho(line, fg=color)


@click.command()
@click.argument('site_url')
def run(site_url):
    validate_url(site_url)


if __name__ == "__main__":
    run()
