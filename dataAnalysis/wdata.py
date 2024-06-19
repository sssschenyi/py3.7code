import xlwt

# 指定要写入的Excel文件名
filename = 'ctl.xls'

# 检查文件是否存在，如果不存在则创建一个Workbook
try:
    # 尝试打开现有的Excel文件
    book = xlwt.Workbook(encoding='utf-8', name = filename)
    sheet = book.add_sheet('Sheet1')  # 添加一个工作表
    existing_data = book.get_sheet(0)  # 获取第一个工作表的数据
except FileNotFoundError:
    # 文件不存在，创建一个新的Workbook
    book = xlwt.Workbook()
    sheet = book.add_sheet('Sheet1')

# 假设我们要写入的数据如下
data_to_write = [
    ['Name', 'Age', 'City'],
    ['Alice', 24, 'New York'],
    ['Bob', 27, 'Los Angeles'],
    ['Charlie', 22, 'San Francisco']
]

# 写入数据到工作表
for row_num, row_data in enumerate(data_to_write):
    for col_num, col_data in enumerate(row_data):
        # 写入数据到指定的单元格
        sheet.write(row_num, col_num, col_data)

# 保存工作簿
book.save(filename)