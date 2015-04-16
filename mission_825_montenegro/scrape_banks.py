import re
from datetime import datetime

from bs4 import BeautifulSoup
import requests
import simplejson as json

from scraper_utils import extract_licence_number, extract_start_date


def scrape_banks():
    root_url = "http://www.cb-cg.org/index.php?mn1=kontrola_banaka&mn2=bankarski_sistem&mn3=licencirane_banke"

    response = requests.get(root_url)
    html = response.content
    soup = BeautifulSoup(html)

    for bank in soup.find("p", "tekst_naslov").parent.find_all("td", "kursna_lista"):
        popup_link = bank.find("a").get('href')
        link = popup_link.split("'", 2)[1]
        response = requests.get("http://www.cb-cg.org" + link)
        html = response.content
        soup = BeautifulSoup(html)

        raw_data = dict()
        raw_data['source_url'] = "http://www.cb-cg.org" + link
        raw_data['company_name'] = soup.find("td", "kursna_list_naslov").contents[0]
        raw_data['sample_date'] = datetime.now().strftime('%Y-%m-%d')

        licence_root = soup.find_all("strong", text=re.compile("Dozvola za rad"))
        if len(licence_root) is 0:
            licence_root = soup.find_all("strong", text=re.compile("Licence no"))
        licence = licence_root[0].next_sibling
        raw_data['licence_number'] = extract_licence_number(licence)
        raw_data['start_date'] = extract_start_date(licence)
        raw_data['address'] = licence_root[0].previous_sibling.previous_sibling

        extract_board_directors(raw_data, soup)

        extract_executive_directors(raw_data, soup)

        extract_audit_comitee(raw_data, soup)

        print json.dumps(raw_data, unicode)


def extract_board_directors(raw_data, soup):
    board_directors = dict()
    members = []
    for board_director in soup.find_all("ol")[0].find_all("li"):
        chairman_found = False
        for chairman_title in [u" - predsjednik Odbora direktora", u" - predsjednik Odbora", u" \u2013 predsjednik", u" - Chairman of the Board"]:
            if chairman_title in board_director.text:
                chairman_found = True
                board_directors['chairman'] = board_director.text.replace(chairman_title, "").strip("\n ")
                break
        if not chairman_found:
            members.append(board_director.text.strip("\n "))
    board_directors['members'] = members
    raw_data['board_directors'] = board_directors


def extract_executive_directors(raw_data, soup):
    executive_directors = dict()
    members = []
    for executive_director in soup.find_all("ol")[1].find_all("li"):
        ceo_found = False
        for ceo_title in [u"- glavni izvr\u0161ni direktor", u" \u2013 glavni izvr\u0161ni direktor", u" \u2013 Glavni izvr\u0161ni direktor", u", glavni izvr\u0161ni direktor", u" - Chief Executive Officer"]:
            if ceo_title in executive_director.text:
                ceo_found = True
                executive_directors['CEO'] = executive_director.text.replace(ceo_title, "").strip("\n ")
                break
        if not ceo_found:
            members.append(executive_director.text.strip("\n "))
    executive_directors['members'] = members
    raw_data['executive_directors'] = executive_directors


def extract_audit_comitee(raw_data, soup):
    if soup.find(text="Odbor za reviziju:"):
        audit_committee = dict()
        members = soup.find_all("ol")[2].find_all("li")
        audit_committee['members'] = map(lambda x: x.text.strip("\n "), members)
        raw_data['audit_committee'] = audit_committee


if __name__ == '__main__':
    scrape_banks()