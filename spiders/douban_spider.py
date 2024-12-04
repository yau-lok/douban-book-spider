from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from utils.logger import setup_logger
from config.settings import CRAWLER_SETTINGS, DOUBAN_SETTINGS

logger = setup_logger()

class DoubanBookSpider:
    def __init__(self, headless=False):
        """初始化爬虫"""
        try:
            print("正在初始化浏览器...")
            self.options = webdriver.ChromeOptions()
            self._setup_browser_options(headless)
            
            # 使用 webdriver_manager 自动安装和管理 ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.options)
            self.wait = WebDriverWait(self.driver, CRAWLER_SETTINGS['TIMEOUT'])
            print("浏览器初始化完成")
            
        except Exception as e:
            print(f"浏览器初始化失败: {str(e)}")
            raise
    
    def _setup_browser_options(self, headless):
        """设置浏览器选项"""
        # 基本设置
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        # 设置用户代理
        self.options.add_argument(f'user-agent={CRAWLER_SETTINGS["USER_AGENT"]}')
        
        # 无头模式设置
        if headless:
            self.options.add_argument('--headless')

    def get_book_info(self, isbn):
        """获取图书信息"""
        try:
            url = f'{DOUBAN_SETTINGS["BASE_URL"]}{isbn}/'
            print(f"访问页面: {url}")
            self.driver.get(url)
            time.sleep(2)  # 等待页面加载
            
            book_info = {}
            
            # 获取书名
            try:
                book_info['title'] = self.driver.find_element(By.XPATH, '//h1/span').text.strip()
                print(f"获取到书名: {book_info['title']}")
            except NoSuchElementException:
                print("未找到书名")
                book_info['title'] = "未找到"

            # 获取详细信息
            try:
                info_text = self.driver.find_element(By.ID, 'info').text
                info_dict = self._parse_info_text(info_text)
                
                # 提取具体信息
                book_info.update({
                    'author': info_dict.get('作者', '未找到'),
                    'publisher': info_dict.get('出版社', '未找到'),
                    'publish_date': info_dict.get('出版年', '未找到'),
                    'pages': info_dict.get('页数', '未找到'),
                    'price': info_dict.get('定价', '未找到'),
                    'binding': info_dict.get('装帧', '未找到'),
                    'isbn': info_dict.get('ISBN', isbn)
                })
                
                print("成功获取图书详细信息")
                return book_info
                
            except NoSuchElementException:
                print(f"获取图书详细信息失败")
                return None
                
        except TimeoutException:
            print(f"页面加载超时")
            return None
        except Exception as e:
            print(f"获取信息时发生错误: {str(e)}")
            return None

    def _parse_info_text(self, info_text):
        """解析图书信息文本"""
        info_dict = {}
        for line in info_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                info_dict[key.strip()] = value.strip()
        return info_dict

    def close(self):
        """关闭浏览器"""
        try:
            self.driver.quit()
            print("浏览器已关闭")
        except Exception as e:
            print(f"关闭浏览器时发生错误: {str(e)}") 