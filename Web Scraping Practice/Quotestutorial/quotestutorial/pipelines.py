# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class QuotestutorialPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("myquotes.db")
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.cur.execute("""create table quotes_tb(
                title text,
                author text,
                tags text

            )""")


    def process_item(self, item, spider):
        self.store_db(item)
        # print("Pipeline :" + item['title'][0])
        return item

    def store_db(self, item):
        self.cur.execute("""insert into quotes_tb values ( ?, ?, ? )""",(
            item['title'][0],
            item['author'][0],
            item['tags'][0]
        ))
        self.conn.commit()