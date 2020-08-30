'''
@Author Caso_卡索
@Date 2020-8-30 15:00
@Func 爬虫程序用到的请求头信息及文件路径信息
'''
Host = "blog.csdn.net" # 请求头host参数
User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
Source = 'html.txt'   # 临时保存博客列表html源码
EachSource = 'each.txt' # 临时保存每篇博客html源码
OUTPUT = "博客信息.csv"  # 输出博客信息到 csv 文件