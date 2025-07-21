import scrapy
import re
import time
import sys
from lotto649.items import LottoItem
import json
from pkylib.utils import mdy_to_ymd, weekday_to_number

class ExampleSpider(scrapy.Spider):
    name = "run649"
    #allowed_domains = ["example.com"]
    #start_urls = ["https://www.national-lottery.com/canada-6-49/results/2022-archive"]
    #start_urls = ['http://quotes.toscrape.com/']

    
    #def start_requests(self):
    async def start(self):

        urls = []
  
        for next_page in range(1982, 2026):
            
            link = 'https://www.national-lottery.com/canada-6-49/results/' + str(next_page) + '-archive'
            # print(f'url = {link}')
            #yield response.follow(next_page, callback=self.parse)
            urls.append(link)


        for url in urls:
            print(f'url = {url}')
            # input('next?')
            yield scrapy.Request(url=url, callback=self.parse)
            pass

    
    def parse(self, response):

        # Access the headers of the request that generated this response
        print('=====================================================')
        # print("Request Headers:")
        # for key, value in response.request.headers.items():
        #     #print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")
        #     print(f"{key}: {value}")

        # #print(f'RESPONSE: {response.body}')
        # title = response.css('title::text').get()
        # print(f'title = {title}')
        # print('=====================================================')

        #
        # 로또정보 가져오기
        #
        table = response.css('table.table.lotto.mobFormat.mobResult')
        trs = table.css('tr')
        print('TR COUNT = ', len(trs), type(trs))

        # remove header
        del trs[0]  
        
        tr = trs[0]
        #print(tr)
        print('-------------------------------------')

        for tr in trs:
            
            # 광고제외
            tr_class = tr.css('tr::attr(class)').get()
            if tr_class != 'noBox':

                first_row = [ el.strip() for el in tr.xpath('td[1]//text()').getall() if el.strip() ]
                print(first_row[0], '==', first_row[1])

                ## 두번째 요소에서 번호 추출
                second_row = [ el.strip() for el in tr.xpath('td[2]//text()').getall() if el.strip() ]
                print(second_row)

                ## 상금액
                money = tr.css('td:nth-child(3)::text').get()
                cleaned_text = re.sub(r'[\n\r\t]', '', money)
                #print('cleaned_text =', cleaned_text)

                ## 1등 배출여부
                #print(tr.css('td:nth-child(4) span::text').get())

                ymd = mdy_to_ymd(first_row[1])
                ymd_split = ymd.split('-')

                item = LottoItem()
                item['year']    = ymd_split[0]
                item['month']   = ymd_split[1]
                item['day']     = ymd_split[2]
                item['weekday'] = weekday_to_number(first_row[0])
                item['number']  = json.dumps(second_row[:6])
                item['bonus']   = second_row[6]

                #print(item)

                # python_object = json.loads(item['number'])

                # print(type(python_object))
                # print(python_object)
                # print(python_object[0], python_object[2])

                yield item


        
        # Follow pagination links
        #url = 'https://www.national-lottery.com/canada-6-49/results/' + 2024 + '-archive'
        #next_page = response.css('li.next a::attr(href)').get()
        #input('go to next?')
        #time.sleep(10)
        # for next_page in range(1982, 2025):
            
        #     url = 'https://www.national-lottery.com/canada-6-49/results/' + str(next_page) + '-archive'
        #     print(f'url = {url}')
        #     #yield response.follow(next_page, callback=self.parse)
        #     yield scrapy.Request(url=url, callback=self.parse)


