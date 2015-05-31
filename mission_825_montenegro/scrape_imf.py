import re
from datetime import datetime

from bs4 import BeautifulSoup
import requests
import simplejson as json

from scraper_utils import extract_licence_number, extract_start_date


def scrape_imf():
    root_url = "http://www.cb-cg.org/index.php?mn1=kontrola_banaka&mn2=bankarski_sistem&mn3=licencirane_mfi"
    response = requests.get(root_url)
    html = response.content
    soup = BeautifulSoup(html)

    imf = soup.find_all("strong", text=re.compile("Dozvola za rad"))
    for imf in imf:
        imf_root = imf.parent.parent.parent.parent
        raw_data = dict()
        raw_data['source_url'] = root_url
        raw_data['sample_date'] = datetime.now().strftime('%Y-%m-%d')
        raw_data['company_name'] = imf_root.find_all("td", "kursna_list_naslov")[0].text
        raw_data['licence_number'] = extract_licence_number(imf.next_sibling)
        raw_data['start_date'] = extract_start_date(imf.next_sibling)
        raw_data['jurisdiction_classification'] = "Micro finance institution"

        print json.dumps(raw_data, unicode)


if __name__ == '__main__':
    scrape_imf()