# encoding: utf-8
"""
用户行为流水表月表 t_data_aimei_user_action_yyyymm;
@author Yuriseus
@create 2016-8-17 17:05
"""
from datetime import datetime
from sqlalchemy import Integer, Column, Text, String, BigInteger, DateTime
from db.db_sqlalchemy import BaseModel
from util.date import DateUtil


class UserAction(object):

    _mapper = {}

    @staticmethod
    def model(goods_id):
        month = DateUtil.now('%Y%m')
        class_name = 'UserAction%s' % month

        ModelClass = UserAction._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (BaseModel,), {
                '__module__': __name__,
                '__name__': class_name,
                '__tablename__': 't_data_aimei_user_action_%s' % month,

                'id': Column(Integer, primary_key=True),
                'uid': Column(Integer),
                'p_type': Column(String(1)),
                't_type': Column(String(1)),
                'a_type': Column(String(1)),
                'action_time': Column(BigInteger),
                'location': Column(Integer),
                'aimei_object': Column(String(64)),
                'update_time': Column(DateTime, default=datetime.now, onupdate=datetime.now)
            })
            UserAction._mapper[class_name] = ModelClass

        cls = ModelClass()
        cls.goods_id = goods_id
        return cls


if __name__ == '__main__':
    user_action = UserAction.model(1)
    connect = user_action.connect
# 新增插入
# gdm = GoodsDesc.model(goods_id)
# gdm.goods_desc = 'desc'
# db.session.add(gd)
#
# # 查询
# gdm = GoodsDesc.model(goods_id)
# gd = gdm.query.filter_by(goods_id=goods_id).first()

# conn.execute(MyTable.insert(), [{'color': 'blue'},
#                                 {'color': 'red'},
#                                 {'color': 'green'}])
