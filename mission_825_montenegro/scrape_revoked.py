import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from scraper_utils import extract_start_date, extract_licence_number


def scrape_revoked():
    root_url = "http://www.cb-cg.org/index.php?mn1=kontrola_banaka&mn2=bankarski_sistem&mn3=banke_u_stecaju_i_likvidaciji"
    response = requests.get(root_url)
    html = response.content
    soup = BeautifulSoup(html)

    for revoked_bank in soup.find_all("a", id=lambda x: x and x.startswith('banka')):
        revoked_bank_root = revoked_bank.parent.parent.parent
        raw_data = dict()
        raw_data['source_url'] = root_url
        raw_data['company_name'] = revoked_bank.next_sibling.replace(u" u likvidaciji", "").replace(u" u ste\u010daju", "")
        if u"u likvidaciji" in revoked_bank.next_sibling:
            raw_data['reason_revoked'] = "liquidation"
        elif u"u ste\u010daju" in revoked_bank.next_sibling:
            raw_data['reason_revoked'] = "bankruptcy"
        raw_data['sample_date'] = datetime.now().strftime('%Y-%m-%d')
        raw_data['status'] = "revoked"
        raw_data['address'] = revoked_bank_root.find("td", "kursna_lista").p.br.next_sibling
        licence = revoked_bank_root.find(text=re.compile("br\. ([0-9-/]+) od ([0-9\.]+)"))
        raw_data['start_date'] = extract_start_date(licence)
        raw_data['licence_number'] = extract_licence_number(licence)
        print json.dumps(raw_data, unicode)


if __name__ == '__main__':
    scrape_revoked()