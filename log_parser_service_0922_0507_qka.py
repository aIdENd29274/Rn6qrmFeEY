# 代码生成时间: 2025-09-22 05:07:58
import sanic
from sanic.response import json, file
from sanic.exceptions import ServerError, NotFound, InvalidUsage
import os
from datetime import datetime
import re

# 定义一个简单的日志解析函数
def parse_log_content(log_content):
    # 使用正则表达式匹配日志中的日期和错误信息
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (ERROR|INFO|WARNING): (.*)')
    parsed_logs = []
    for line in log_content.splitlines():
        match = pattern.match(line)
        if match:
            date, level, message = match.groups()
            parsed_logs.append({'date': date, 'level': level, 'message': message})
    return parsed_logs

# 创建Sanic应用app = sanic.Sanic('LogParserService')

# 定义路由，用于上传日志文件@app.route('/upload', methods=['POST'])
def upload_log(request):
    file = request.file('file')
    if not file:
        raise InvalidUsage('No file provided', status_code=400)
    try:
        log_content = file.file.read().decode('utf-8')
        parsed_logs = parse_log_content(log_content)
        return json({'status': 'success', 'parsed_logs': parsed_logs})
    except Exception as e:
        raise ServerError(f'Failed to parse log file: {e}', status_code=500)

# 定义路由，用于下载解析后的日志文件@app.route('/download/<filename>')
def download_log(request, filename):
    try:
        file_path = f'./parsed_logs/{filename}'
        if not os.path.exists(file_path):
            raise NotFound('File not found')
        return file(file_path, filename=filename)
    except Exception as e:
        raise ServerError(f'Failed to download log file: {e}', status_code=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)