"""
Hip Hop Wikipedia Scraper.

Scrapes the hip hop pages of Wikipedia for upcoming
release dates of new albums and singles.

Currently only supports albums.
"""

import requests
from bs4 import BeautifulSoup

# Setup BS4
url = 'https://en.wikipedia.org/wiki/2016_in_hip_hop_music'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
tables = soup.findAll('table', attrs={'class': 'wikitable'})

# Used to identify a date entry in a table row
DATE_IDENTIFIER = 'td[rowspan]'
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


def get_date_and_releases(row):
    """Return the first album date found in a table row."""
    items = row.findAll('td')
    for item in items:
        if item.has_attr('rowspan'):
            return (item.text, item['rowspan'])
    else:
        return (items[0].text, 1)

# Begin scrape
albums = []
rowspans = []
multiple_releases = False
releases_left = 0

table = tables[0].findAll(['tr'])[1:]  # Cut out the <th> element
for row in table:
    if not multiple_releases:
        data = get_date_and_releases(row)
        release_date = data[0]
        releases_left = int(data[1])
        print(release_date, ' - Releases: ', releases_left)
        print('--------------------------')

    if releases_left > 1:
        multiple_releases = True
    elif releases_left == 1:
        multiple_releases = False

    releases_left -= 1

    # Extract artist and album
    content = row.findAll('td')
    if content[0].text.split()[0] in MONTHS:
        content = content[1:3]
    else:
        content = content[:2]
    print(content[0].text, ' - ', content[1].text)

    # Separator between days
    if releases_left == 0:
        print('\n')
