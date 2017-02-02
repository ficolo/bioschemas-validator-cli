import urllib2
from extruct.w3cmicrodata import MicrodataExtractor
from validator import validate_item
import settings
import click


def validate_url(site_url):
	response = urllib2.urlopen(site_url)
	html = response.read()
	mde = MicrodataExtractor()
	data = mde.extract(html)
	for item in data['items']:
		if item['type'] in settings.supported_types:
			click.secho('ITEM RETRIEVED: ' + str(item), fg='blue')
			click.secho('VALIDATION OUTPUT: ' + str(validate_item(item)), fg='red', bold=True)

@click.command()
@click.argument('site_url')
def run(site_url):
	validate_url(site_url)


if __name__ == "__main__":
	run()