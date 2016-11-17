# encoding: utf-8
"""
web server
@author Yuriseus
@create 2016-11-16 00:53
"""

import web
from eship.db import DBSqlite
from excel_util import ExcelUtil


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


class Export(object):
    def __init__(self):
        pass

    def save_to_excel(self):
        excel_path = '/home/dream/github/study/eship/ship.xlsx'
        data_list = []
        title = ['编号', '鉴定机构', '船名', '船型', '建造日期', '建造船厂', '船籍港', '总长（米）', '型宽（米）',
                 '型深（米）', '总吨', '载重吨', '船级', '航区', '主机型号', '成交日期', '鉴证日期', '成交价格（元）', '卖出方',
                 '查询网址']
        data_list.append(title)
        ships = service.get_ship_by_sql("select * from ship_cj")
        for ship in ships:
            data = [ship['dbid'], ship['pid'], ship['shipname'], ship['shiptype'], ship['scd'], ship['scp'],
                    ship['sregp'], ship['loa'], ship['bm'], ship['dm'], ship['gt'], ship['dwt'],
                    ship['sclass'], ship['sr'], ship['mt'], ship['cdate'], ship['adate'], ship['price'],
                    ship['seller'], ship['link']]
            data_list.append(data)
        ExcelUtil.write_to_excel(excel_path, data_list)


if __name__ == "__main__":
    # app.run()
    export = Export()
    export.save_to_excel()

