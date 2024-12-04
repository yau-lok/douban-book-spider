import logging
import sys
import os
from datetime import datetime

def setup_logger():
    """配置并返回日志记录器"""
    # 创建logger对象
    logger = logging.getLogger('DoubanSpider')
    logger.setLevel(logging.INFO)

    # 确保logs目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 创建日志文件名（包含时间戳）
    log_filename = f'logs/crawler_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    # 创建文件处理器
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 添加一条启动日志
    logger.info('日志系统初始化完成')

    return logger 