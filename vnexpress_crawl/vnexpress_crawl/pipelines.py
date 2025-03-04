from itemadapter import ItemAdapter
import csv
import logging
import pandas
from pymongo import MongoClient

class MongoDBPipeline:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["vnexpress"]
        self.collection = self.db["crawl"]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

class SaveToCSVPipeline:
    def __init__(self):
        self.filename = f'data/vnexpress_crawl.csv'
        try:
            self.file = open(self.filename, 'w', newline='', encoding='utf-8')
            self.csv_writer = None
            logging.info(f"Created CSV file: {self.filename}")
        except Exception as e:
            logging.error(f"Error creating CSV file: {e}")
            raise
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not self.csv_writer:
            self.csv_writer = csv.DictWriter(self.file, fieldnames=adapter.keys())
            self.csv_writer.writeheader()
            
        self.csv_writer.writerow(adapter.asdict())
        return item
    
    def close_spider(self, spider):
        self.file.close()
        logging.info(f"Closed CSV file: {self.filename}")
        
        
class SaveToExcelPipeline:
    def __init__(self):
        self.items = []
        self.filename = f'data/vnexpress_crawl.xlsx'

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        df = pandas.DataFrame(self.items)
        df.to_excel(self.filename, index=False, engine='openpyxl')

class TxtPipeline:
    def open_spider(self, spider):
        self.file = open("vnexpress_crawl.txt", "w", encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write(f"URL: {item['url']}\n")
        self.file.write(f"Title: {item['title']}\n")
        self.file.write(f"Time: {item['time']}\n")
        self.file.write(f"Author: {item['author']}\n")
        self.file.write(f"Category: {item['category']}\n")
        self.file.write(f"Content: {item['content']}\n")
        self.file.write(f"Tags: {item['tags']}\n")
        self.file.write(f"Comments: {item['comments']}\n")
        self.file.write("="*50 + "\n")
        return item

    def close_spider(self, spider):
        self.file.close()
