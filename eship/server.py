# encoding: utf-8
"""
web server
@author Yuriseus
@create 2016-11-16 00:53
"""

import web
from eship.db import DBSqlite

urls = (
    "/.*", "Index"
)

app = web.application(urls, globals())


class ShipService(object):
    def __init__(self):
        self.db_path = '/home/dream/github/study/eship/eship/eship.db'
        self.db = DBSqlite(self.db_path)

    def get_ship_by_sql(self, sql):
        return self.db.fetchall(sql)

service = ShipService()


class Index:
    def GET(self):
        ships = service.get_ship_by_sql("select * from ship limit 10")
        return str(ships)

if __name__ == "__main__":
    app.run()
