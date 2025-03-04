import scrapy
import json
from vnexpress_crawl.items import VnexpressItem

class VnexpressSpider(scrapy.Spider):
    name = "vnexpress_crawl"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/phap-luat/ho-so-pha-an"]

    def parse(self, response):
        articles = response.css('article.item-news')
        if not articles:
            self.logger.warning("Không tìm thấy bài viết nào!")

        for article in articles:
            title = article.css('h2.title-news a::text').get()
            url = article.css('h2.title-news a::attr(href)').get()
            
            if url:
                yield response.follow(url, self.parse_article, meta={"title": title, "url": url})

    def parse_article(self, response):
        item = VnexpressItem()
        
        # Trích xuất JSON-LD (schema.org)
        json_ld_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if json_ld_data:
            try:
                data = json.loads(json_ld_data)
                
                # Cập nhật dữ liệu từ JSON-LD
                item["url"] = data.get("mainEntityOfPage", {}).get("@id", response.url)
                item["title"] = data.get("headline", "Không có tiêu đề")
                item["time"] = data.get("datePublished")
                item["author"] = data.get("author", {}).get("name", "Không rõ")
                item["category"] = ", ".join(data.get("about", [])) if isinstance(data.get("about"), list) else data.get("about")
                item["content"] = data.get("description", "").strip()
                item["tags"] = data.get("keywords", "")

                # Trích xuất ảnh đại diện
                item["image_url"] = data.get("image", {}).get("url", "")
            except json.JSONDecodeError:
                self.logger.warning("Lỗi phân tích JSON-LD, sử dụng XPath thay thế!")

        # Nếu không có JSON-LD, fallback sang XPath
        if not item.get("title"):
            item["url"] = response.meta["url"]
            item["title"] = response.meta["title"].strip() if response.meta["title"] else "Không có tiêu đề"
            item["time"] = response.xpath('//span[@class="date"]/text()').get()
            item["author"] = response.xpath('//p[@class="author_mail"]/text()').get()
            item["category"] = response.xpath('//ul[@class="breadcrumb"]/li[last()]/a/text()').get()

            content = response.xpath('//article//p//text()').getall()
            item["content"] = " ".join([text.strip() for text in content if text.strip()])

            item["tags"] = response.xpath('//meta[@name="keywords"]/@content').get()

        # Trích xuất bình luận
        comments = response.xpath('//div[@class="content-comment"]/p[@class="full_content"]/text()').getall()
        item["comments"] = "; ".join([comment.strip() for comment in comments if comment.strip()])

        yield item

