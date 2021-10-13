from types import MethodType
import scrapy
from scrapy.http.request import Request

from biPro.items import BiproItem
class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # allowed_domains = ['www.xxx.com']
    # 开始的域名
    start_urls = ['https://www.bilibili.com/v/popular/rank/all']

    def parse(self, response):
        li_list=response.xpath('//*[@id="app"]/div/div[2]/div[2]/ul/li[@class="rank-item"]')
        for li in li_list:
            content_url="https:"+li.xpath(".//div[@class='info']/a/@href").extract_first()
            name=li.xpath(".//div[@class='info']/a/text()").extract_first()
            item=BiproItem()
            item['name']=name
            yield scrapy.Request(url=content_url,callback=self.video_parse,meta={'item':item})
    def video_parse(self,response):
        item=response.meta['item']
        url = response.selector.re(r'"base_url":"(.*?)"')  # 匹配视频，音频地址
        item['video_url']=url[0]
        item['sound_url']=url[-1]
        yield item
       