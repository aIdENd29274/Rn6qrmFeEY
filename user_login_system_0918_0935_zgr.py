# 代码生成时间: 2025-09-18 09:35:40
import json
from sanic import Sanic, response
from sanic.response import json as sanic_json
from sanic.exceptions import ServerError, ClientError, ValidationError

# 假设的用户数据库，实际应用中应使用数据库存储
USER_DATABASE = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}

app = Sanic("UserLoginSystem")

# 用户登录接口
@app.route("/login", methods=["POST"])
async def login(request):
    # 获取请求体中的用户名和密码
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # 验证用户名和密码
    if not username or not password:
        return sanic_json({"error": "Username and password are required."}, status=400)

    user = USER_DATABASE.get(username)
    if not user or user["password"] != password:
        return sanic_json({"error": "Invalid username or password."}, status=401)

    # 登录成功，返回成功信息和用户信息
    return sanic_json({"message": "Login successful.", "user": user}, status=200)

# 启动服务器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
