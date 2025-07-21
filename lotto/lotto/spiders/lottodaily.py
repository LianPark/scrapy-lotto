import scrapy
import json
import logging
from lotto.items import LottoItem
from pkylib.utils import mdy_to_ymd, get_weekday_from_date

class LottodailySpider(scrapy.Spider):
    name = "lottodaily"
    allowed_domains = ["example.com"]
    start_urls = ["https://www.playnow.com/services2/lotto/draw/latest"]

    def parse(self, response):

        lottomax = {}

        json_data = response.body
        json_dict = json.loads(response.body)

        # 보기좋게 프린트 하는 방법
        #pretty_json = json.dumps(json_dict, indent=4)
        #print(pretty_json)

        item = LottoItem()

        item['lmax'] = self.make_dict(json_dict['LMAX']['drawDate'], json_dict['LMAX']['drawNbrs'], json_dict['LMAX']['bonusNbr'])
        item['bc49'] = self.make_dict(json_dict['BC49']['drawDate'], json_dict['BC49']['drawNbrs'], json_dict['BC49']['bonusNbr'])
        item['dgrd'] = self.make_dict(json_dict['DGRD']['drawDate'], json_dict['DGRD']['drawNbrs'], json_dict['DGRD']['bonusNbr'])
        item['six49'] = self.make_dict(json_dict['SIX49']['drawDate'], json_dict['SIX49']['drawNbrs'], json_dict['SIX49']['bonusNbr'])

        print('ITEM = ',item)

        yield item


    def make_dict(self, date, num, bonus):

        item = dict()

        ymd = mdy_to_ymd(date, '%b %d, %Y')
        ymd_split = ymd.split('-')

        item['year']    = int(ymd_split[0])
        item['month']   = int(ymd_split[1])
        item['day']     = int(ymd_split[2])

        item['weekday'] = get_weekday_from_date(ymd)

        item['number']  = json.dumps(num)
        item['bonus']   = bonus


        return item



