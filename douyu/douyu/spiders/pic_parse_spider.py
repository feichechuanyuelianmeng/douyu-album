import scrapy
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from scrapy_demo.douyu.douyu.items import DouyuItem

# import  selenium.webdriver.remote.webelement.WebElement

class PicParseSpiderSpider(scrapy.Spider):

    name = 'pic_parse.spider'
    allowed_domains = ['www.douyu.com']
    start_urls = ["https://www.douyu.com/g_yz"]

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"D:\programs\chrome_driver\chromedriver.exe")

    def parse(self, response):

        self.driver.get(self.start_urls[0])
        # 得到总的页数page
        page = self.get_total_page()
        # 不断点击下一页并获得所有主播房间url存放到列表urls中
        urls = self.get_all_urls(page)# 在这里调节到底要爬取多少主播的相册
        # 根据url获取图片信息
        for url in urls:
            item = self.get_pic_item(url)
            time.sleep(1)
            yield item

    # 获取页数
    def get_total_page(self):
        """获取所有页数"""

        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located
                                                          ((By.XPATH,
                                                            "/html/body/section/main/section[2]/div[2]/div/ul/li[last()-1]")))
            page = int(element.text)
            return page
        except:
            print("获取页数失败")
    # 获得所有主播链接地址
    def get_all_urls(self,page):
        urls = []
        try:
            for i in range(page):
                time.sleep(1)
                li_lsit = self.driver.find_elements_by_xpath("/html/body/section/main/section[2]/div[2]/ul/li")
                test_num = 1
                for li in li_lsit:
                    try:
                        url = li.find_element_by_xpath("./div/a[1]").get_attribute("href")
                        # print("第{}页的url:".format(i + 1) + url)
                        # print("正在爬取第：{}页总共{}页主播房间的url".format((i+1),(page+1)))
                        urls.append(url)
                        # break
                        # 爬取5个人的
                        i = i + 1
                        if i == 5:
                            break

                    except:
                        pass
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located
                                                              ((By.XPATH,
                                                                "/html/body/section/main/section[2]/div[2]/div/ul/li[last()]")))
                return urls
                # 点击下一页

                element.click()
                time.sleep(1)
                # test
                break


        except:
            print("没有下一页了或者没有加载成功")
    # 进入链接后点击相册
    def click_photo_album(self,url):
        self.driver.get(url)
        # time.sleep(3)

        try:
            name_ele = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located
                                                           ((By.XPATH,
                                                             "/html/body/section/main/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/h2")))
        except:
            print("获取名字超时")
        # name_ele = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located
        #                                                    ((By.XPATH,
        #                                                      "/html/body/section/main/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/h2")))

        name = name_ele.text
        # time.sleep(1)
        # element = self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[1]/div/div/div/div[1]/a[4]")
        # 等待frame出现
        try:
            iframe_test = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located
                                                               ((By.TAG_NAME,
                                                                 "iframe")))
        except:
            print("获取页面超时")

        # time.sleep(10)
        # iframe_test = self.driver.find_element_by_tag_name("iframe")
        # # iframe_test = self.driver.find_element_by_xpath("//iframe[title='test']")
        # print(iframe_test)

        # 切换页面并沉睡
        self.driver.switch_to.frame(iframe_test)
        time.sleep(1)
        # 相册按钮
        try:
            element = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located
                                                           ((By.XPATH,
                                                             "/html/body/div/div/div/div/div[1]/div/div/div/div[1]/a[4]")))
        except:
            print("获取相册按钮超时")

        # element = self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[1]/div/div/div/div[1]/a[4]")
        # self.driver.switch_to.default_content()
        # print(element.text)
        element.click()
        return name
        time.sleep(1)
    #点击更多图片加载进来
    def click_more(self):
        try:
            more_pic = self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div/div/div")
            while more_pic:
                print(more_pic.text)
                time.sleep(0.5)
                more_pic.click()
                time.sleep(1)
                more_pic = self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div/div/div")
                time.sleep(1)
        except:
            pass
    # 下载所有图片
    def get_all_pic(self,name):
        src_list = []
        # try:
        #     pic_urls = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located
        #                                                     ((By.XPATH,
        #                                                       "/html/body/div/div/div/div/div[2]/div/a")))
        #     print("可以获取图片url", pic_urls)
        #     if pic_urls is not None:
        #         for pic in pic_urls:
        #             # print("图片详情页")
        #             # print(type(pic))
        #             time.sleep(3)
        #             img_url = pic.find_element_by_xpath("./img")
        #             print("获取单个图片：", img_url)
        #
        # except:
        #     print("获取图片按钮超时")

        try:
            # print("进入获取图片链接")

            pic_urls = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div[2]/div/a")
            time.sleep(1)
            if pic_urls is not None:
                for pic in pic_urls:
                    # print("图片详情页")
                    # print(type(pic))
                    img_url = pic.find_element_by_xpath("./img")
                    # time.sleep(2)
                    src = img_url.get_attribute("src")
                    src = src.split("?")[0]
                    print("正在爬取主播：{} 的图片:{}".format(name, src))
                    src_list.append(src)
        except:
            pass
        item = DouyuItem(image_urls=src_list, name=name)
        print("主播{}的相册爬取完成！！！！".format(name))
        # print(item)
        return item
    def get_pic_item(self,url):
        try:
            # 点击页面的相册按钮
            name = self.click_photo_album(url)
            # 点击更多按钮让图片都加载出来
            self.click_more()
            # 得到图片信息并返回
            item = self.get_all_pic(name)
            return item
        except:
            print("该房间进不去！！！！！")










