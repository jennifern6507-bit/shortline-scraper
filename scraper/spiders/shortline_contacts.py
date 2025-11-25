import scrapy
import re
import requests

from utils.pdf_parser import parse_pdf_from_bytes
from utils.text_cleaner import clean_text
from utils.contact_extractor import extract_contacts, extract_address

class ShortlineContactSpider(scrapy.Spider):
    name = "shortline_contacts"

    start_urls = [
        "https://www.railserve.com/Railroad_Directory/Short_Line/",
        "https://www.aslrra.org/our-members/",
    ]

    def parse(self, response):
        links = response.css("a::attr(href)").getall()

        for link in links:
            if any(x in link.lower() for x in ["rail", "rr", "railroad", "railway"]):
                yield response.follow(link, self.parse_company)

    def parse_company(self, response):
        raw_text = response.text

        emails = list(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw_text)))
        phones = list(set(re.findall(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}", raw_text)))

        contacts = extract_contacts(raw_text)
        address = extract_address(raw_text)

        pdf_links = [x for x in response.css("a::attr(href)").getall() if x.lower().endswith(".pdf")]

        pdf_text = ""
        for pdf_url in pdf_links:
            try:
                full = response.urljoin(pdf_url)
                pdf_bytes = requests.get(full, timeout=10).content
                pdf_text += parse_pdf_from_bytes(pdf_bytes) + "\n"
            except:
                pass

        pdf_text = clean_text(pdf_text)
        pdf_contacts = extract_contacts(pdf_text)
        pdf_address = extract_address(pdf_text)

        for role in contacts:
            if contacts[role] is None and pdf_contacts[role] is not None:
                contacts[role] = pdf_contacts[role]

        if not address and pdf_address:
            address = pdf_address

        yield {
            "url": response.url,
            "emails": emails,
            "phones": phones,
            "hq_address": address,
            "contacts": contacts,
            "pdfs_checked": pdf_links,
        }
