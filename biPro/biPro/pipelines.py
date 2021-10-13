# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import subprocess

from itemadapter import ItemAdapter
import os


class BiproPipeline:
    def process_item(self, item, spider):
        name=item['name']
        base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        shi_video=base_path+name+"1.mp4"
        yin_video = base_path + name + "2.mp4"
        filename=name+".mp4"
        cmd = f'ffmpeg -i {yin_video} -i {shi_video} -acodec copy -vcodec copy {filename}'
        print(cmd)
        subprocess.call(cmd, shell=True)

from scrapy.pipelines.files import FilesPipeline
import scrapy
class VideoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        """Returns the media requests to download"""
        return scrapy.Request(url=item['video_url'],meta={"item":item})
    def file_path(self, request, response=None, info=None, *, item=None):

        item=request.meta['item']
        file_path=r"{name}1.mp4".format(name=item["name"])
        print(file_path)
        return file_path
    def item_completed(self, results, item, info):
        return item

class soundPipeline(FilesPipeline):
    def get_media_requests(self,item, info):
        return scrapy.Request(url=item['sound_url'],meta={"item":item})
    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        file_path=r"{name}2.mp4".format(name=item["name"])
        print(file_path)
        return file_path
    def item_completed(self,results,item, info):
        return item

