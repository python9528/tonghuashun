import scrapy


class Gupiao(scrapy.Spider):
    name = 'gupiao'
    start_urls = ['http://stock.10jqka.com.cn/']
    def parse(self, response):
        a_list = response.xpath('//div[@id="rzrq"]/table[@class="m-table"]/tbody/tr/td[2]/a')
        num = 1
        for a in a_list:
            url_str = a.xpath('./@href').extract()[0]
            ajax_num = response.xpath('//div[@id="rzrq"]/table[@class="m-table"]/tbody/tr[%d]/td[1]/a/text()'%num).extract()[0]
            gp_name = a.xpath('./text()').extract()[0] + '.txt'
            yield scrapy.Request(url_str,callback=self.download_data,meta={'gp_name':gp_name,'go':1,'ajax_num':ajax_num})
            num += 1

    def download_data(self,response):
        tr_list = response.xpath('//table[@class="m-table"]/tbody/tr')
        gp_name = response.meta['gp_name']
        go = response.meta['go']
        ajax_num = response.meta['ajax_num']
        if go == 1:
            num = response.xpath('//div[@class="m-page J-ajax-page"]/span/text()').extract()[0].split('/')[1]
            for i in range(2, int(num) + 1):
                ajax = 'http://data.10jqka.com.cn/market/rzrqgg/code/%s/order/desc/page/%s/ajax/1/' % (ajax_num,str(i))
                yield scrapy.Request(ajax, callback=self.download_data, meta={'gp_name': gp_name,'go':'1','ajax_num':ajax_num})

        for tr in tr_list:
            td_list = tr.xpath('.//td/text()').extract()
            td_list[1] =td_list[1].strip()
            with open(gp_name,'a') as f:
                f.write(' + '.join(td_list) + '\n')

