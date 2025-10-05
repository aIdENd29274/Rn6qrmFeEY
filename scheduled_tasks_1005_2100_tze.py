# 代码生成时间: 2025-10-05 21:00:48
import asyncio
from sanic import Sanic, response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor

# 创建Sanic应用
app = Sanic("Scheduled Tasks")
scheduler = AsyncIOScheduler(AsyncIOExecutor())
scheduler.start()

# 定时任务函数，用于执行一些周期性任务
async def scheduled_task():
    # 这里添加你需要执行的定时任务代码
    print("Scheduled task is running...")

# 添加定时任务到调度器
scheduler.add_job(scheduled_task, trigger=CronTrigger(hour=0, minute=0))  # 每小时执行一次

# Sanic路由，用于启动定时任务
@app.route("/start_task")
async def start_task(request):
    try:
        # 确保定时任务只添加一次
        if not scheduler.get_jobs():
            scheduler.add_job(scheduled_task, trigger=CronTrigger(hour=0, minute=0))
        return response.json({"message": "Task started successfully"})
    except Exception as e:
        return response.json({"error": str(e)})

# Sanic路由，用于停止定时任务
@app.route("/stop_task")
async def stop_task(request):
    try:
        jobs = scheduler.get_jobs()
        if jobs:
            for job in jobs:
                scheduler.remove_job(job.id)
            return response.json({"message": "Task stopped successfully"})
        else:
            return response.json({"message": "No tasks to stop"})
    except Exception as e:
        return response.json({"error": str(e)})

# Sanic路由，用于获取定时任务状态
@app.route("/task_status")
async def task_status(request):
    jobs = scheduler.get_jobs()
    return response.json({"status": "running" if jobs else "stopped"})

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
