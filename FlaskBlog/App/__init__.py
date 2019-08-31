from flask import Flask
from .views import blog, admin
from  .exts import init_exts


def create_app():
    app = Flask(__name__)

    #配置数据库
    db_uri ='mysql+pymysql://root:root@localhost:3306/flaskblog'      #本地数据库配置
    # db_uri ='mysql+pymysql://root:root@120.24.176.130:3306/flaskblog'   #远程数据库配置
    app.config['SQLALCHEMY_DATABASE_URI']=db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #以后默认禁用，这里应该开启

    app.register_blueprint(blueprint=blog)  #注册蓝图
    app.register_blueprint(blueprint=admin)
    init_exts(app)#初始化插件

    return app