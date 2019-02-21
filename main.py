from scrapy_spider import ProductsSpider
from scrapy.crawler import CrawlerProcess
from database_connection import MySQLDatabase
from datetime import datetime, timedelta
from create_report import Report
import sys

def start_crawling():
    
    process = CrawlerProcess()
    input_file = sys.argv[1] if len(sys.argv) > 1 else "eComm_crawler.xlsm"
    process.crawl(ProductsSpider, file = input_file)
    process.start()
    
def generate_report():
    
    db = MySQLDatabase()
    
    current_date = datetime.now()
    previous_date = current_date - timedelta(1)
    
    current_records = db.fetch_current_records(current_date)
    oos_data = db.fetch_oos_data(current_date)
    price_diff_data = db.fetch_price_diff_data(current_date, previous_date)
    
    r = Report(f"SummaryReportOn{current_date.strftime('%d-%m-%Y')}.html")
    
    r.generate_report_content("Summary", ['Last Run', 'Total Records'], [[f"{current_date.strftime('%d-%m-%Y %H:%M:%S')}", str(current_records)],])
    r.generate_report_content("Out of Stocks", ['eRetailer', 'Url'], oos_data)
    r.generate_report_content("Price Difference", ['eRetailer', 'Title', f"Price on {previous_date.strftime('%d-%m-%Y')}", "Current Price"], price_diff_data)
    
    r.create_html_report()
    
    db.close()
    
if __name__ == '__main__':
    
    try:
        start_crawling()
        generate_report()
    except Exception as e:
        print(e)
    