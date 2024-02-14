from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sys

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
# 使用了flash 因此需要设置秘钥
# 这里os.getenv的作用是优先使用本地环境 如果没有则使用后面的默认参数
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev') # 等同于 app.secret_key = 'dev'
# SQLite的URI sqlite:////数据库文件的绝对地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login' # 重定向到登录页

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchList.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。
# 上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
    from watchList.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}

from watchList import routers, commands



