import mysql.connector as db
from settings import MYSQL_HOSTNAME, MYSQL_USERNAME, MYSQL_DATABASE, \
                    MYSQL_UNICODE, MYSQL_CHARSET, MYSQL_TABLENAME, MYSQL_PASSWORD

class MySQLDatabase:

    def __init__(self):
        
        try:
            self.db_con = db.connect(
                    host = MYSQL_HOSTNAME,
                    user = MYSQL_USERNAME,
                    database = MYSQL_DATABASE,
                    password = MYSQL_PASSWORD,
                    use_unicode = MYSQL_UNICODE,
                    charset = MYSQL_CHARSET
                )
            self.cur = self.db_con.cursor(buffered=True)
        except (AttributeError, db.OperationalError) as e:
            print(e)
    
    def insert_data(self, eretailer, title, price, currency, url):
        
        query = f"INSERT INTO {MYSQL_TABLENAME} \
                    (eretailer, title, price, currency, url) \
                    VALUES(%s, %s, %s, %s, %s)"
        self.cur.execute(query, (eretailer, title, price, currency, url))
        
    def fetch_current_records(self, current_date):
        
        query = f"SELECT * FROM {MYSQL_TABLENAME} \
                        WHERE DATE(INSERTED_ON) = DATE('{current_date}')"
        self.cur.execute(query)
        return len(self.cur.fetchall())

    def fetch_oos_data(self, current_date):
        
        query = f"SELECT DISTINCT ERETAILER, URL FROM {MYSQL_TABLENAME} \
                        WHERE DATE(INSERTED_ON) = DATE('{current_date}') \
                        AND (PRICE IS NULL OR TITLE IS NULL)"
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def fetch_price_diff_data(self, current_date, previous_date):
        
        query = f"SELECT CURR.ERETAILER, CURR.TITLE, PREV.PRICE, CURR.PRICE \
                    FROM \
                        (SELECT * FROM {MYSQL_TABLENAME} WHERE date(INSERTED_ON) = date('{current_date}')) CURR \
                        INNER JOIN \
                        (SELECT * FROM {MYSQL_TABLENAME} WHERE date(INSERTED_ON) = date('{previous_date}')) PREV \
                        ON CURR.URL = PREV.URL \
                    WHERE CURR.PRICE <> PREV.PRICE"
        self.cur.execute(query)
        return self.cur.fetchall()

    def commit(self):
        
        self.db_con.commit()

    def close(self):
        
        self.cur.close()
        self.db_con.close()
