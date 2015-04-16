# -*- coding: utf-8 -*-

import turbotlib

from scrape_banks import scrape_banks
from scrape_foreign import scrape_foreign
from scrape_imf import scrape_imf
from scrape_revoked import scrape_revoked


turbotlib.log("Starting run")

turbotlib.log("\nScraping banks :")
scrape_banks()

turbotlib.log("\nScraping IMFs :")
scrape_imf()

turbotlib.log("\nScraping foreign banks :")
scrape_foreign()

turbotlib.log("\nScraping revoked banks :")
scrape_revoked()

