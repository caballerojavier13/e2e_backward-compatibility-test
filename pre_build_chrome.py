import os
import requests
from jinja2 import FileSystemLoader, Environment, select_autoescape

url = 'https://api.github.com/repos/caballerojavier13/chrome-downloads/contents/x64.deb'

querystring = {'ref': 'master'}

payload = ''
headers = {
    'Authorization': 'token ' + os.environ['GITHUB_TOKEN'],
    'Accept': 'application/json',
    'cache-control': 'no-cache'
}

response = requests.request('GET', url, data=payload, headers=headers, params=querystring)

files = [f for f in response.json() if f['size'] > 2]

processed_versions = []

file_loader = FileSystemLoader('template/chrome-template')
template = Environment(loader=file_loader).get_template('Dockerfile')

chrome_driver_match = {
    '48': '2.21',
    '49': '2.22',
    '50': '2.22',
    '51': '2.23',
    '52': '2.24',
    '53': '2.26',
    '54': '2.27',
    '55': '2.28',
    '56': '2.29',
    '57': '2.29',
    '58': '2.31',
    '59': '2.32',
    '60': '2.33',
    '61': '2.34',
    '62': '2.35',
    '63': '2.36',
    '64': '2.37',
    '65': '2.38',
    '66': '2.40',
    '67': '2.41',
    '68': '2.42',
    '69': '2.44',
    '70': '2.45',
    '71': '2.46',
    '72': '2.46',
    '73': '2.46'
}

print('Start Processing Chrome dockerfiles:\n')

for f in files[::-1]:
    version_number = str(f['name']).split('_')[1].split('.')[0]
    if version_number not in processed_versions:
        processed_versions.append(version_number)
        print("\t Processing Chrome version => %s" % version_number)
        folder_name = "./dist/chrome/selenium_chrome_%s" % version_number

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        dockerfile = template.render(
            google_path=f['download_url'],
            chrome_driver_version=chrome_driver_match[version_number]
        )

        with open(folder_name + '/Dockerfile', 'w') as d:
            d.write(dockerfile)
            d.close()
