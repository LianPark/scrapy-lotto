# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from scrapy.exceptions import DropItem
import json

class LottomaxPipeline:

    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_database):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

        self.is_duplicate = True
        print('2. __init__', self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_database)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_database=crawler.settings.get('MYSQL_DATABASE')
        )

    # This method is called when the spider is opened.
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.mysql_host,
            user=self.mysql_user,
            password=self.mysql_password,
            database=self.mysql_database
        )
        self.cursor = self.conn.cursor()

        ## Create quotes table if none exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lottomax (
                year SMALLINT(11) NOT NULL DEFAULT '0',
                month tinyint(4) NOT NULL DEFAULT 0,
                day tinyint(4) NOT NULL DEFAULT 0,
                weekday tinyint(4) NOT NULL DEFAULT 0,
                number VARCHAR(100),
                bonus VARCHAR(255),
                UNIQUE KEY `date` (`year`,`month`,`day`)
            )
        """)
    
    
    def process_item(self, item, spider):
        """
                
        """
        # 아이템에서 데이터를 추출하여 SQL 쿼리에 사용 : 
        # INSERT INTO lotto649 (year,month,day,weekday,number,bonus) VALUES (%s, %s,%s, %s,%s, %s)


        #
        # lotto649 테이블에 데이타 저장
        #
        try:
            query = """
                INSERT INTO lottomax (year,month,day,weekday,number,bonus) VALUES (%s, %s,%s, %s,%s, %s)
            """
            values = (
                item['year'],
                item['month'],
                item['day'],
                item['weekday'],
                item['number'],
                item['bonus'],
            )
            self.cursor.execute(query, values)
            self.conn.commit()

            self.is_duplicate = False
            
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            #raise DropItem(f"Could not insert item into database: {err}")


        if not self.is_duplicate:
            #
            # countmax 테이블 Main 에 저장
            #
            try:
                num = json.loads(item['number'])
                query = "INSERT INTO countmax (year,type,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`) VALUES ({},'{}',{},{},{},{},{},{},{})".format(
                    num[0],num[1],num[2],num[3],num[4],num[5],num[6],item['year'],'M',1,1,1,1,1,1,1
                )
                #print(query)
                values = (
                    item['year'],
                    item['month'],
                    item['day'],
                    item['weekday'],
                    item['number'],
                    item['bonus'],
                )
                self.cursor.execute(query)
                self.conn.commit()
            except mysql.connector.Error as err:

                #print(f"MySQL Error: {err}")
                query = "UPDATE countmax SET `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1 WHERE year={} and type='M'".format(
                    num[0],num[0],num[1],num[1],num[2],num[2],num[3],num[3],num[4],num[4],num[5],num[5],num[6],num[6],item['year'])
                #print(query)
                self.cursor.execute(query)
                self.conn.commit()
                #print(f"MySQL Error: {err}")
                #raise DropItem(f"Could not insert item into database: {err}")



            # countmax 테이블 Bonus 에 저장
            bonus = item['bonus']
            try:            
                query = "INSERT INTO countmax (year,type,`{}`) VALUES ({},'{}',{})".format(bonus,item['year'],'B',1)
                #print(query)
                self.cursor.execute(query)
                self.conn.commit()
            except mysql.connector.Error as err:

                #print(f"MySQL Error: {err}")
                query = "UPDATE countmax SET `{}`=`{}`+1 WHERE year={} and type='B'".format(bonus, bonus, item['year'])
                #print(query)
                self.cursor.execute(query)
                self.conn.commit()
                #print(f"MySQL Error: {err}")
                #raise DropItem(f"Could not insert item into database: {err}")


            self.is_duplicate = True

        return item


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

