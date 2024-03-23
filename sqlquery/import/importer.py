import pandas as pd
import pymysql

# 读取 Excel 数据
excel_file = 'DemoQuickBuild.xlsx'
df = pd.read_excel(excel_file)

# 连接到 MySQL 数据库
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345678',
                             database='sqldemo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:

        # 将数据插入到数据库
        for index, row in df.iterrows():
            #  INSERT INTO `sqldemo`.`order` (`id`, `order_date`, `order_no`, `client_no`, `company_id`, `catalog_no`, `product_id`, `product_no`, `catalog_name`, `order_quantity`, `product_price`, `order_total`) VALUES (99999, '2024-03-19 14:08:28', '1', '2', '3', '4', '5', '6', '7', '8', 9.00, 10.00);
            sql = f"INSERT INTO order_record (`id`, `order_date`, `order_no`, `client_no`, `company_id`, `catalog_no`, `product_id`, `product_no`, `catalog_name`, `order_quantity`, `product_price`, `order_total`) VALUES ({index}, '{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', {row[8]}, {row[9]}, {row[10]})"
            print(sql)
            cursor.execute(sql)
        connection.commit()
finally:
    connection.close()
