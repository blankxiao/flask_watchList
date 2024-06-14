根据教程[《Flask入门教程》](https://tutorial.helloflask.com/)完成
## **主要功能**:
- 用户认证（注册、登录、注销）
- 添加、编辑和删除电影条目
- 显示电影列表

### 项目结构
```plaintext
watchlist/
  - __init__.py: Flask 应用工厂函数
  - models.py: 数据库模型定义
  - routes.py: 路由定义
  - templates/: 模板文件目录
  - static/: 静态文件目录
- venv/: 虚拟环境目录
- requirements.txt: 依赖包文件
- README.md
```


`git clone https://github.com/blankxiao/flask_watchList.git` 克隆项目
`cd flask_watchList` 进入文件目录
`flask run` 运行项目
在`./watchList/commands,py`文件有定义一些命令，比如`flask initdb`用于初始化数据库等
