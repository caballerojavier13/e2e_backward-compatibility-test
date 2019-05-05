import os
import requests
from lxml.html import document_fromstring 
from jinja2 import FileSystemLoader, Environment, select_autoescape

versions = range(43, 68)

url = 'https://ftp.mozilla.org/pub/firefox/releases/'

resp = requests.get(url=url)

if resp.status_code != 200:
    raise Exception('Something gone wrong')

processed_versions = []

file_loader = FileSystemLoader('template/firefox-template')
template = Environment(loader=file_loader).get_template('Dockerfile')

gecko_driver_match = {
    '43': '0.16.0',
    '44': '0.16.0',
    '45': '0.16.0',
    '46': '0.16.0',
    '47': '0.16.0',
    '48': '0.16.0',
    '49': '0.16.0',
    '50': '0.16.0',
    '51': '0.16.0',
    '52': '0.17.0',
    '53': '0.18.0',
    '54': '0.18.0',
    '55': '0.20.1',
    '56': '0.20.1',
    '57': '0.24.0',
    '58': '0.24.0',
    '59': '0.24.0',
    '60': '0.24.0',
    '61': '0.24.0',
    '62': '0.24.0',
    '63': '0.24.0',
    '64': '0.24.0',
    '65': '0.24.0',
    '66': '0.24.0',
    '67': '0.24.0'
}

print('Start Processing Firefox dockerfiles:\n')

doc = document_fromstring(resp.text)
for tag in doc.cssselect('a')[::-1]:
    text_content = str(tag.text_content())
    try:
        version_number = int(text_content.split('.')[0])
        if version_number in versions and version_number not in processed_versions:
            processed_versions.append(version_number)
            print("\t Processing Firefox version => %s" % version_number)
            folder_name = "./dist/firefox/selenium_firefox_%s" % version_number
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            firefox_url = "https://ftp.mozilla.org%slinux-x86_64/en-US/firefox-%s.tar.bz2" % (
                tag.get('href'), text_content.split('/')[0]
            )

            dockerfile = template.render(
                firefox_url=firefox_url,
                version_number=version_number,
                gecko_driver_version=gecko_driver_match[str(version_number)]
            )

            with open(folder_name + '/Dockerfile', 'w') as d:
                d.write(dockerfile)
                d.close()
    except ValueError:
        pass
