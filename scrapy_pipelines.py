from database_connection import MySQLDatabase

class DataBasePipeline(object):

    def open_spider(self, spider):
        self.db_obj = MySQLDatabase()
    
    def process_item(self, item, spider):
        self.db_obj.insert_data(item['eretailer'], item['title'], item['price'], item['currency'], item['url'])

    def close_spider(self, spider):
        self.db_obj.commit()
        self.db_obj.close()
    