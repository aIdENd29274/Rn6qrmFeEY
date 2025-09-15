# 代码生成时间: 2025-09-16 07:40:47
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
import os
import signal
import psutil

# 定义进程管理器应用
app = Sanic('ProcessManager')

# 定义一个路由，列出所有进程信息
@app.route('/api/processes', methods=['GET'])
async def list_processes(request: Request):
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'status': proc.info['status']
            })
        return response.json(processes)
    except Exception as e:
        raise ServerError('Failed to list processes', e)

# 定义一个路由，终止一个进程
@app.route('/api/processes/<pid:int>', methods=['DELETE'])
async def kill_process(request: Request, pid: int):
    try:
        proc = psutil.Process(pid)
        if not proc.is_running():
            return response.json({'error': 'Process is not running'})
        proc.terminate()
        proc.wait()
        return response.json({'message': 'Process terminated successfully'})
    except psutil.NoSuchProcess:
        return response.json({'error': 'Process does not exist'})
    except psutil.AccessDenied:
        return response.json({'error': 'Access denied to terminate process'})
    except Exception as e:
        raise ServerError('Failed to terminate process', e)

# 定义一个路由，启动一个新的进程
@app.route('/api/processes/start', methods=['POST'])
async def start_process(request: Request):
    try:
        data = request.json
        command = data.get('command')
        if not command:
            return response.json({'error': 'No command provided'})
        # 启动一个新的进程
        process = psutil.Popen(command, shell=True)
        return response.json({'pid': process.pid})
    except Exception as e:
        raise ServerError('Failed to start process', e)

if __name__ == '__main__':
    # 启动Sanic应用
    app.run(host='0.0.0.0', port=8000)