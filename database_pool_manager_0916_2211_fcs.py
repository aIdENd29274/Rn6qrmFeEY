# 代码生成时间: 2025-09-16 22:11:46
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool

# Database configuration
DATABASE_URI = 'your_database_uri_here'

app = Sanic("DatabasePoolManager")

# 创建数据库引擎，使用连接池
engine = create_engine(DATABASE_URI, poolclass=QueuePool, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 异步上下文管理器以获取数据库会话
async def get_session() -> SessionLocal:
    try:
        async with app.ctx.session_scope():
            yield app.ctx.session
    except SQLAlchemyError as e:
        raise ServerError("Database session error", "Internal Server Error", e)

# 确保每个请求都有自己的数据库会话
@app.listener('before_server_start')
async def setup_database(app, loop):
    # 初始化数据库会话上下文
    app.ctx.session_scope = SessionLocal()
    app.ctx.session = None

# 清理数据库会话
@app.listener('after_server_stop')
async def close_database(app, loop):
    if app.ctx.session:
        app.ctx.session.close()

# 示例路由，使用数据库会话
@app.route("/")
async def index(request):
    try:
        # 获取数据库会话
        async with get_session() as session:
            # 执行数据库操作
            result = session.execute("SELECT 1").scalar()
            return response.json({"message": "Hello, world!", "result": result})
    except ServerError as e:
        return response.json({"error": str(e)}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)