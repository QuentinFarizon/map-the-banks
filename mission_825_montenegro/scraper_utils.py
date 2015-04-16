from datetime import datetime
import re


def extract_licence_number(licence):
    matched_license = re.search(r"([0-9-/]+) o", licence)
    return matched_license.group(1)


def extract_start_date(licence):
    matched_start_date = re.search(r"of (.*)", licence)
    if matched_start_date is not None:
        date = datetime.strptime(matched_start_date.group(1), '%d %B %Y')
    else:
        matched_start_date = re.search(r"od ([0-9]*)\. ([a-z]*) ([0-9]*)", licence)
        if matched_start_date is not None:
            # See doc of month_to_number
            date = datetime(int(matched_start_date.group(3)),
                            month_to_number(matched_start_date.group(2)),
                            int(matched_start_date.group(1)))
            return date.strftime('%Y-%m-%d')
        else:
            matched_start_date = re.search(r"od ([0-9]{2}\.[0-9]{2}\.[0-9]{4})", licence)
            if matched_start_date is not None:
                date = datetime.strptime(matched_start_date.group(1), '%d.%m.%Y')
            else:
                date = None
    return date.strftime('%Y-%m-%d')


# No serbian locale sr_* contained the month names used in the site
# I haven't found much documentation nor references about serbian month names
# The first form ('mart') seems to be advised, but the site use the second form ('marta')
# So I'm putting both in case they decide to change at some point
# I have found the first form here : http://www.digitalnaagenda.gov.rs/lat/arhiva/
# I have found the second form used in http://www.aarau.ch/documents/Info_serbisch_ODLAGANJE_I_ODVOZENJE_OTPADA-2015.pdf
def month_to_number(month):
    return {'januar': 1,
            'januara': 1,
            'februar': 2,
            'februara': 2,
            'mart': 3,
            'marta': 3,
            'april': 4,
            'aprila': 4,
            'maj': 5,
            'maja': 5,
            'jun': 6,
            'juna': 6,
            'jul': 7,
            'jula': 7,
            'avgust': 8,
            'avgusta': 8,
            'septembar': 9,
            'septembra': 9,
            'oktobar': 10,
            'oktobra': 10,
            'novembar': 11,
            'novembra': 11,
            'decembar': 12,
            'decembra': 12,
            }.get(month, 0)
