# 爬虫设置
CRAWLER_SETTINGS = {
    'DELAY': 3,  # 爬取间隔（秒）
    'TIMEOUT': 10,  # 页面加载超时时间（秒）
    'HEADLESS': False,  # 是否使用无头模式
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# 输出设置
OUTPUT_SETTINGS = {
    'CSV_FILE': 'book_info.csv',  # CSV输出文件名
    'ENCODING': 'utf-8-sig',  # 文件编码（支持Excel打开）
    'COLUMNS': [
        'title',     # 书名
        'author',    # 作者
        'publisher', # 出版社
        'publish_date', # 出版年
        'pages',     # 页数
        'price',     # 定价
        'binding',   # 装帧
        'isbn'       # ISBN
    ]
}

# 日志设置
LOG_SETTINGS = {
    'LEVEL': 'INFO',  # 日志级别
    'FORMAT': '%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    'DIRECTORY': 'logs',  # 日志目录
    'ENCODING': 'utf-8'  # 日志文件编码
}

# 豆瓣网站设置
DOUBAN_SETTINGS = {
    'BASE_URL': 'https://book.douban.com/isbn/',
    'SEARCH_URL': 'https://book.douban.com/subject_search?search_text=',
    'HEADERS': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
}

# 错误重试设置
RETRY_SETTINGS = {
    'MAX_RETRIES': 3,  # 最大重试次数
    'RETRY_DELAY': 5,  # 重试间隔（秒）
} 