import pymysql

import secret
import config
from models.__init__ import SQLModel
from models.comment import Comment
from models.session import Session
from models.user_role import UserRole
from models.user import User
from models.todo_ajax import TodoAjax
from models.weibo import Weibo


def recreate_table(cursor):
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    cursor.execute(TodoAjax.sql_create)
    cursor.execute(Weibo.sql_create)
    cursor.execute(Comment.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'DROP DATABASE IF EXISTS `{}`'.format(
                    config.db_name
                )
            )
            cursor.execute(
                'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                    config.db_name
                )
            )
            cursor.execute('USE `{}`'.format(config.db_name))

            recreate_table(cursor)

        connection.commit()
    finally:
        connection.close()


def test_data():
    SQLModel.init_db()


    form = dict(
        username='test',
        password='123',
        role=UserRole.normal,
    )
    u, result = User.register(form)

    Session.add(u.id)

    form = dict(
        title='test todo',
        user_id=u.id,
    )
    t = TodoAjax.new(form)

    form = dict(
        content='test_weibo',
        user_id=u.id,
    )

    w = Weibo.new(form)

    form = dict(
        content='test_comment',
        user_id=u.id,
        weibo_id=1,
    )

    w = Comment.new(form)

    # SQLModel.connection.close()


if __name__ == '__main__':
    recreate_database()
    test_data()
