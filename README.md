# Shortline Railroad Contact Scraper

A Scrapy-powered crawler that extracts:
- CEO / President / GM
- Procurement contacts
- Maintenance of Way (MOW)
- Engineering contacts
- HQ address
- Emails / Phones
- PDF parsing

Run:
```
pip install -r requirements.txt
scrapy crawl shortline_contacts -o results.json
```