# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from scrapy.exceptions import DropItem
import json
import logging

class LottoPipeline:

    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_database):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

        self.is_new = False

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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotto649 (
                year SMALLINT(11) NOT NULL DEFAULT '0',
                month tinyint(4) NOT NULL DEFAULT 0,
                day tinyint(4) NOT NULL DEFAULT 0,
                weekday tinyint(4) NOT NULL DEFAULT 0,
                number VARCHAR(100),
                bonus VARCHAR(255),
                UNIQUE KEY `date` (`year`,`month`,`day`)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lottobc (
                year SMALLINT(11) NOT NULL DEFAULT '0',
                month tinyint(4) NOT NULL DEFAULT 0,
                day tinyint(4) NOT NULL DEFAULT 0,
                weekday tinyint(4) NOT NULL DEFAULT 0,
                number VARCHAR(100),
                bonus VARCHAR(255),
                UNIQUE KEY `date` (`year`,`month`,`day`)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lottogrand (
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

        #logging.info(f"Crawled URL: process_item")

        self.insert_data_to_db('lottobc', item['bc49'])
        self.insert_data_to_db('lottogrand', item['dgrd'])
        self.insert_data_to_db('lottomax', item['lmax'])
        self.insert_data_to_db('lotto649', item['six49'])

        return item
    


    def insert_data_to_db(self, prefix, item):

        try:
            query = "INSERT INTO {} (year,month,day,weekday,number,bonus) VALUES (%s, %s,%s, %s,%s, %s)".format(prefix)
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

            self.is_new = True
            
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            #raise DropItem(f"Could not insert item into database: {err}")


        num = json.loads(item['number'])
        bonus = item['bonus']
        if prefix == 'lottomax':

            query = "INSERT INTO countmax (year,type,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`) VALUES ({},'{}',{},{},{},{},{},{},{})".format(
                    num[0],num[1],num[2],num[3],num[4],num[5],num[6],item['year'],'M',1,1,1,1,1,1,1
            )
            query_bonus = "INSERT INTO countmax (year,type,`{}`) VALUES ({},'{}',{})".format(bonus,item['year'],'B',1)
            query_bonus_update = "UPDATE countmax SET `{}`=`{}`+1 WHERE year={} and type='B'".format(bonus, bonus, item['year'])

        elif prefix == 'lotto649':

            query = "INSERT INTO count649 (year,type,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`) VALUES ({},'{}',{},{},{},{},{},{})".format(
                    num[0],num[1],num[2],num[3],num[4],num[5],item['year'],'M',1,1,1,1,1,1
            )
            query_bonus = "INSERT INTO count649 (year,type,`{}`) VALUES ({},'{}',{})".format(bonus,item['year'],'B',1)
            query_bonus_update = "UPDATE count649 SET `{}`=`{}`+1 WHERE year={} and type='B'".format(bonus, bonus, item['year'])

        elif prefix == 'lottobc':

            query = "INSERT INTO countbc (year,type,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`) VALUES ({},'{}',{},{},{},{},{},{})".format(
                    num[0],num[1],num[2],num[3],num[4],num[5],item['year'],'M',1,1,1,1,1,1
            )
            query_bonus = "INSERT INTO countbc (year,type,`{}`) VALUES ({},'{}',{})".format(bonus,item['year'],'B',1)
            query_bonus_update = "UPDATE countbc SET `{}`=`{}`+1 WHERE year={} and type='B'".format(bonus, bonus, item['year'])

        elif prefix == 'lottogrand':

            query = "INSERT INTO countgrand (year,type,`{}`,`{}`,`{}`,`{}`,`{}`) VALUES ({},'{}',{},{},{},{},{})".format(
                    num[0],num[1],num[2],num[3],num[4],item['year'],'M',1,1,1,1,1
            )
            query_update = "UPDATE countmax SET `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1, `{}`=`{}`+1 WHERE year={} and type='M'".format(
                    num[0],num[0],num[1],num[1],num[2],num[2],num[3],num[3],num[4],num[4],item['year'])
            query_bonus = "INSERT INTO countgrand (year,type,`{}`) VALUES ({},'{}',{})".format(bonus,item['year'],'B',1)
            query_bonus_update = "UPDATE countgrand SET `{}`=`{}`+1 WHERE year={} and type='B'".format(bonus, bonus, item['year'])


        if self.is_new:
            #
            # countmax 테이블 Main 에 저장
            #
            try:
                self.cursor.execute(query)
                self.conn.commit()
            except mysql.connector.Error as err:

                self.cursor.execute(query_update)
                self.conn.commit()


            # countmax 테이블 Bonus 에 저장
            try:
                self.cursor.execute(query_bonus)
                self.conn.commit()
            except mysql.connector.Error as err:
                self.cursor.execute(query_bonus_update)
                self.conn.commit()
                #print(f"MySQL Error: {err}")
                #raise DropItem(f"Could not insert item into database: {err}")

            self.is_new = True


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()