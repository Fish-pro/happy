"""
启动和管理相关操作代码
通过Manager管理项目，通过migrate增加数据迁移
"""

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()  # 创建对象
manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manage.run()