import sys
import json

while True:
    line = sys.stdin.readline()
    if not line:
        break
    raw_record = json.loads(line)

    licence_record = {
        "company_name": raw_record['company_name'],
        "source_url": raw_record['source_url'],
        "sample_date": raw_record['sample_date'],
        "start_date": raw_record['start_date'],
        "licence_number": raw_record['licence_number'],
        "status": raw_record.get("status", "Current"),
        "jurisdiction_classification": 'Bank',
        "category": 'Financial',
        "confidence": 'HIGH',
        "company_jurisdiction": "Montenegro",
        "licence_jurisdiction": "Montenegro",
        "regulator": "Centralna Banka Crne Gore"
        }

    print json.dumps(licence_record)

