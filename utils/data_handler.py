import pandas as pd
import os
import logging
from datetime import datetime

logger = logging.getLogger('DoubanSpider')

class DataHandler:
    """数据处理类，用于处理Excel输入和CSV输出"""
    
    @staticmethod
    def read_excel_isbns(file_path):
        """
        从Excel文件读取ISBN列表
        :param file_path: Excel文件路径
        :return: ISBN列表
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 读取Excel文件第一列
            logger.info(f"正在读取Excel文件: {file_path}")
            df = pd.read_excel(file_path, usecols=[0])
            
            # 转换为字符串并处理
            isbns = df.iloc[:, 0].astype(str).str.strip()
            
            # 清理数据
            isbns = isbns[isbns.str.len() >= 10]  # 只保留长度大于等于10的ISBN
            isbns = isbns.str.replace('-', '')    # 移除可能的连字符
            isbns = isbns.str.replace('.0', '')   # 移除Excel可能添加的小数点
            
            # 转换为列表并去重
            isbn_list = list(set(isbns.tolist()))
            
            logger.info(f"成功读取 {len(isbn_list)} 个有效ISBN")
            return isbn_list
            
        except Exception as e:
            logger.error(f"读取Excel文件失败: {str(e)}")
            raise

    @staticmethod
    def save_to_csv(book_info_list, output_file):
        """
        保存图书信息到CSV文件
        :param book_info_list: 图书信息列表
        :param output_file: 输出文件名
        """
        try:
            if not book_info_list:
                logger.warning("没有数据需要保存")
                return False
                
            # 创建DataFrame
            df = pd.DataFrame(book_info_list)
            
            # 设置列的顺序
            columns = ['title', 'author', 'publisher', 'publish_date', 
                      'pages', 'price', 'binding', 'isbn']
            df = df.reindex(columns=columns)
            
            # 重命名列
            column_names = {
                'title': '书名',
                'author': '作者',
                'publisher': '出版社',
                'publish_date': '出版年',
                'pages': '页数',
                'price': '定价',
                'binding': '装帧',
                'isbn': 'ISBN'
            }
            df = df.rename(columns=column_names)
            
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name, file_ext = os.path.splitext(output_file)
            output_file_with_timestamp = f"{file_name}_{timestamp}{file_ext}"
            
            # 保存为CSV
            df.to_csv(output_file_with_timestamp, 
                     index=False, 
                     encoding='utf-8-sig')  # 使用带BOM的UTF-8编码，以支持Excel正确显示中文
            
            logger.info(f"数据已保存到文件: {output_file_with_timestamp}")
            return True
            
        except Exception as e:
            logger.error(f"保存CSV文件失败: {str(e)}")
            raise

    @staticmethod
    def validate_isbn(isbn):
        """
        验证ISBN号码是否有效
        :param isbn: ISBN号码
        :return: 清理后的ISBN或None
        """
        if not isbn:
            return None
            
        # 清理ISBN
        isbn = str(isbn).strip()
        isbn = isbn.replace('-', '').replace(' ', '')
        
        # 移除Excel可能添加的.0
        if isbn.endswith('.0'):
            isbn = isbn[:-2]
        
        # 简单的长度验证
        if len(isbn) < 10 or len(isbn) > 13:
            return None
            
        return isbn