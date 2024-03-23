from flask import Flask, request, jsonify
import pymysql.cursors
import logging
app = Flask(__name__)

# 配置日志记录级别
app.logger.setLevel(logging.DEBUG)

# 创建一个日志输出的处理器，输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# 将处理器添加到日志中
app.logger.addHandler(console_handler)

# 加载配置
app.config.from_pyfile('config.cfg')

# 连接 MySQL 数据库
connection = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/query', methods=['POST'])
def execute_query():
    try:
        app.logger.debug('args:')
        app.logger.debug(request.args)
        app.logger.debug('json:')
        app.logger.debug(request.json)
        # 获取 POST 请求中的 SQL 查询字符串
        sql_query = request.json.get('sqlquery')
        app.logger.debug('sqlquery')
        app.logger.debug(sql_query)
        app.logger.debug(type(sql_query))
        the_sql =  sql_query[0]['generated_text']
        app.logger.debug('the_sqlquery')
        app.logger.debug(the_sql)
        app.logger.debug(type(the_sql))
        the_sql= the_sql.replace('\n', ' ')
        the_sql = the_sql.replace('```sql', '')
        the_sql = the_sql.replace('```', '')
        app.logger.debug('the_sqlquery')
        app.logger.debug(the_sql)
       # 执行 SQL 查询
        with connection.cursor() as cursor:
            cursor.execute(the_sql)
            result = cursor.fetchall()
            app.logger.debug('result')
            app.logger.debug(result)
        return jsonify({'success': True, 'data': result}), 200

    except Exception as e:
        app.logger.error('error')
        app.logger.error(e)
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089)