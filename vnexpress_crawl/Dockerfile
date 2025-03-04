# Sử dụng Python 3.9 làm base image
FROM python:3.9

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy toàn bộ Scrapy project vào container
COPY ../scrapy_app/ /app/

# Cài đặt các package cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Lệnh chạy Scrapy spider khi container khởi động
CMD ["scrapy", "crawl", "my_spider"]
