import scrapy
import json
from pkylib.utils import mdy_to_ymd, get_weekday_from_date
from lottomax.items import LottomaxItem

class RunmaxSpider(scrapy.Spider):
    name = "runmax"
    allowed_domains = ["lottomaxnumbers.com"]
    #start_urls = ["https://www.lottomaxnumbers.com/numbers/2010"]


    async def start(self):

        urls = []
  
        for next_page in range(2009, 2026):
            
            link = 'https://www.lottomaxnumbers.com/numbers/' + str(next_page)
            urls.append(link)

        for url in urls:
            #print(f'url = {url}')
            # input('next?')
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        trs = response.css('table.archiveResults.mobFormat > tbody > tr')
        for i, tr in enumerate(trs,start=1):

            if i != 5:
                date = tr.xpath('td[1]/a/text()').get()
                num  = [ el.strip() for el in tr.xpath('td[2]//text()').getall() if el.strip() ]

                win   = num[:-1]
                bonus = num[-1]
                print(i, date, win, bonus)

                ymd = mdy_to_ymd(date)
                weekday = get_weekday_from_date(ymd)

                ymd_split = ymd.split('-')

                item = LottomaxItem()
                item['year']    = ymd_split[0]
                item['month']   = ymd_split[1]
                item['day']     = ymd_split[2]
                item['weekday'] = weekday
                item['number']  = json.dumps(win)
                item['bonus']   = bonus

                yield item

        pass
