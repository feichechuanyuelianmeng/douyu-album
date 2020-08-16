# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
from scrapy_demo.douyu.douyu import settings
from scrapy.pipelines.images import ImagesPipeline
import os


# class DouyuPipeline:
#     def __init__(self):
#         self.fp =open("url.json", 'wb')
#         self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.fp.close()

# 实现图片的分类别存储
class DouyuPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(DouyuPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            # print("得到的请求是："+request)
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(DouyuPipeline, self).file_path(request, response, info)
        name = request.item.get("name")
        store = settings.IMAGES_STORE
        name_path = os.path.join(store, name)
        if not os.path.exists(name_path):
            # 如果不存在url那么就不创建文件加

            os.makedirs(name_path)

        image_name = path.replace("full/", "")
        image_path = os.path.join(name_path, image_name)

        return image_path


