import json
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from scraper_utils import extract_licence_number, extract_start_date


def scrape_foreign():
    root_url = "http://www.cb-cg.org/index.php?mn1=kontrola_banaka&mn2=bankarski_sistem&mn3=predstavnistva"
    response = requests.get(root_url)
    html = response.content
    soup = BeautifulSoup(html)

    for foreign_bank in soup.find_all("a", id=lambda x: x and x.startswith('banka')):
        foreign_bank_root = foreign_bank.parent.parent.parent
        raw_data = dict()
        raw_data['source_url'] = root_url
        raw_data['company_name'] = foreign_bank.next_sibling
        raw_data['sample_date'] = datetime.now().strftime('%Y-%m-%d')
        licence = foreign_bank_root.find_all("li")[0].text
        raw_data['licence_number'] = extract_licence_number(licence)
        raw_data['start_date'] = extract_start_date(licence)
        raw_data['address'] = foreign_bank_root.find(text=re.compile("Adresa.*"))\
            .next_sibling.next_sibling.next_sibling.strip("- ")
        director = foreign_bank_root.find(text=re.compile("Predsjednik"))
        raw_data['director'] = director.replace(u" \u2013 Predsjednik", "").strip("- ")
        raw_data['executives'] = extract_executives(director)

        print json.dumps(raw_data, unicode)


def extract_executives(director):
    executives = director.parent.find_all(text=re.compile("- "))[1:]
    return map(lambda ex: ex.strip("- "), executives)


if __name__ == '__main__':
    scrape_foreign()
