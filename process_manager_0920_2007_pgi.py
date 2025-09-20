# 代码生成时间: 2025-09-20 20:07:52
import asyncio
import subprocess
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError, ServerNotRunning
from sanic.log import logger
import psutil


# 定义 ProcessManager 类
class ProcessManager:
    """进程管理器，用于启动、停止和监控进程"""
    def __init__(self):
        self.processes = {}

    def start_process(self, name, command):
        """根据命令启动进程并存储到字典中"""
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes[name] = process
            logger.info(f"Process {name} started with PID: {process.pid}")
            return process.pid
        except Exception as e:
            logger.error(f"Failed to start process {name}: {e}")
            raise ServerError(message=f"Failed to start process {name}")

    def stop_process(self, name):
        """根据进程名称停止进程"""
        try:
            if name in self.processes:
                process = self.processes.pop(name)
                process.terminate()
                process.wait()
                logger.info(f"Process {name} stopped")
                return True
            else:
                raise ServerError(message=f"Process {name} not found")
        except Exception as e:
            logger.error(f"Failed to stop process {name}: {e}")
            raise ServerError(message=f"Failed to stop process {name}")

    def restart_process(self, name):
        """重启进程"""
        try:
            if name in self.processes:
                self.stop_process(name)
                self.start_process(name, self.processes[name].cmd)
                logger.info(f"Process {name} restarted")
                return True
            else:
                raise ServerError(message=f"Process {name} not found")
        except Exception as e:
            logger.error(f"Failed to restart process {name}: {e}")
            raise ServerError(message=f"Failed to restart process {name}")

    def get_process_info(self, name):
        """获取进程信息"""
        try:
            if name in self.processes:
                process = self.processes[name]
                info = {
                    "name": name,
                    "pid": process.pid,
                    "status": psutil.Process(process.pid).status(),
                    "cpu_percent": psutil.Process(process.pid).cpu_percent(),
                    "memory_percent": psutil.Process(process.pid).memory_percent(),
                }
                return info
            else:
                raise ServerError(message=f"Process {name} not found")
        except Exception as e:
            logger.error(f"Failed to get process info for {name}: {e}")
            raise ServerError(message=f"Failed to get process info for {name}")


# 创建 Sanic 应用
app = Sanic("Process Manager")
process_manager = ProcessManager()

# 定义启动进程的路由
@app.route("/start/<name>/<command:path>", methods=["POST"])
async def start_process(request: Request, name, command):
    """启动进程"""
    try:
        pid = process_manager.start_process(name, command)
        return response.json({
            "message": f"Process {name} started with PID: {pid}",
            "pid": pid,
        })
    except ServerError as e:
        return response.json({"error": str(e)})

# 定义停止进程的路由
@app.route("/stop/<name>", methods=["POST"])
async def stop_process(request: Request, name):
    """停止进程"""
    try:
        result = process_manager.stop_process(name)
        return response.json({
            "message": f"Process {name} stopped" if result else "Process not found",
        })
    except ServerError as e:
        return response.json({"error": str(e)})

# 定义重启进程的路由
@app.route("/restart/<name>", methods=["POST"])
async def restart_process(request: Request, name):
    """重启进程"""
    try:
        result = process_manager.restart_process(name)
        return response.json({
            "message": f"Process {name} restarted" if result else "Process not found",
        })
    except ServerError as e:
        return response.json({"error": str(e)})

# 定义获取进程信息的路由
@app.route("/info/<name>", methods=["GET"])
async def get_process_info(request: Request, name):
    """获取进程信息"""
    try:
        process_info = process_manager.get_process_info(name)
        return response.json(process_info)
    except ServerError as e:
        return response.json({"error": str(e)})


if __name__ == "__main__":
    # 运行 Sanic 应用
    app.run(host="0.0.0.0", port=8000, debug=True)