import os
import sys
import time
from spiders.douban_spider import DoubanBookSpider
from config.settings import CRAWLER_SETTINGS, OUTPUT_SETTINGS
from utils.logger import setup_logger
from utils.data_handler import DataHandler

# 初始化日志
logger = setup_logger()

def get_isbns_from_input():
    """从用户输入获取ISBN"""
    isbns = []
    print("\n请输入ISBN号码（每行一个，输入空行结束）：")
    while True:
        try:
            isbn = input().strip()
            if not isbn:
                if isbns:  # 如果已经输入了至少一个ISBN才退出
                    break
                else:
                    print("请至少输入一个ISBN")
                    continue
            
            isbn = DataHandler.validate_isbn(isbn)
            if isbn:
                isbns.append(isbn)
                print(f"已添加ISBN: {isbn}")
            else:
                print(f"警告: 无效的ISBN格式，请重新输入")
        except KeyboardInterrupt:
            print("\n已取消输入")
            break
    return isbns

def main():
    try:
        print("\n=== 豆瓣图书信息爬虫程序 ===")
        print("1. 手动输入ISBN")
        print("2. 从Excel文件读取ISBN")
        
        while True:
            choice = input("\n请选择输入方式 (1 或 2): ").strip()
            if choice in ['1', '2']:
                break
            print("无效的选择，请输入1或2")
        
        isbn_list = []
        if choice == '1':
            isbn_list = get_isbns_from_input()
        else:
            while True:
                file_path = input("\n请输入Excel文件的完整路径: ").strip()
                try:
                    isbn_list = DataHandler.read_excel_isbns(file_path)
                    break
                except Exception as e:
                    print(f"读取文件失败: {str(e)}")
                    retry = input("是否重试？(y/n): ").strip().lower()
                    if retry != 'y':
                        return
        
        if not isbn_list:
            print("未获取到有效的ISBN，程序退出")
            return
            
        print(f"\n共获取到 {len(isbn_list)} 个ISBN")
        print("开始爬取数据...")
        
        spider = DoubanBookSpider(headless=CRAWLER_SETTINGS['HEADLESS'])
        results = []
        
        try:
            for i, isbn in enumerate(isbn_list, 1):
                print(f"\n正在处理第 {i}/{len(isbn_list)} 个ISBN: {isbn}")
                book_info = spider.get_book_info(isbn)
                if book_info:
                    results.append(book_info)
                    print(f"成功获取《{book_info['title']}》的信息")
                else:
                    print(f"获取ISBN {isbn} 的信息失败")
                
                if i < len(isbn_list):
                    delay = CRAWLER_SETTINGS['DELAY']
                    print(f"等待 {delay} 秒后继续...")
                    time.sleep(delay)
        
            if results:
                DataHandler.save_to_csv(results, OUTPUT_SETTINGS['CSV_FILE'])
                print(f"\n爬取完成！共获取 {len(results)} 本图书的信息")
            else:
                print("\n未成功获取任何图书信息")
                
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            print(f"爬取过程中发生错误: {str(e)}")
        finally:
            print("\n正在关闭浏览器...")
            spider.close()
            
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        import traceback
        print("错误详情:")
        print(traceback.format_exc())
    finally:
        print("\n程序结束")
        input("按回车键退出...")

if __name__ == "__main__":
    main() 