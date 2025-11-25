import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("scraped_contacts.json", "w")
        self.file.write("[")

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item, indent=2) + ","
        self.file.write(line)
        return item
