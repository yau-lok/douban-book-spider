# 豆瓣图书信息爬虫

一个基于 Selenium 的豆瓣图书信息爬虫程序，支持通过 ISBN 批量获取图书信息。

## 功能特点

- 支持手动输入 ISBN 和 Excel 文件批量导入
- 自动获取书名、作者、出版社等信息
- 结果保存为 CSV 文件，支持 Excel 打开
- 详细的日志记录
- 自动管理 ChromeDriver

## 安装依赖 
pip install -r requirements.txt


## 使用方法

1. 克隆仓库：
git clone https://github.com/你的用户名/douban-book-spider.git

cd douban-book-spider

2. 安装依赖：

pip install -r requirements.txt

3. 运行程序：

python main.py


## 输入方式

1. 手动输入 ISBN
   - 每行输入一个 ISBN
   - 输入空行结束

2. Excel 文件导入
   - ISBN 放在第一列
   - 支持 xls 和 xlsx 格式

## 输出结果

程序会生成包含以下信息的 CSV 文件：
- 书名
- 作者
- 出版社
- 出版年
- 页数
- 定价
- 装帧
- ISBN

## 注意事项

- 请遵守豆瓣的使用规则
- 建议适当设置爬取间隔
- 确保网络连接正常

## 致谢

感谢以下开源项目：
- Selenium
- Pandas
- webdriver_manager

感谢Cursor！本脚本完全由Cursor编写。