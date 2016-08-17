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


class UserAction(BaseModel):

    # _mapper = {}

    __tablename__ = 't_data_aimei_user_action_201608'

    id = Column(Integer(), primary_key=True)
    uid = Column(Integer)
    p_type = Column(String(1))
    t_type = Column(String(1))
    a_type = Column(String(1))
    action_time = Column(BigInteger())
    location = Column(Integer())
    aimei_object = Column(String(64))
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    @classmethod
    def get_table_name(cls, column_value):
        return 't_data_aimei_user_action_%s' % DateUtil.now('%Y%m')

    # @classmethod
    # def model(cls, value_dict=None):
    #     month = DateUtil.now('%Y%m')
    #     class_name = 'UserAction%s' % month
    #
    #     ModelClass = UserAction._mapper.get(class_name, None)
    #     if ModelClass is None:
    #         ModelClass = type(class_name, (BaseModel,), {
    #             '__module__': __name__,
    #             '__name__': class_name,
    #             '__tablename__': 't_data_aimei_user_action_%s' % month,
    #
    #             'id': Column(Integer(), primary_key=True),
    #             'uid': Column(Integer()),
    #             'p_type': Column(String(1)),
    #             't_type': Column(String(1)),
    #             'a_type': Column(String(1)),
    #             'action_time': Column(BigInteger()),
    #             'location': Column(Integer()),
    #             'aimei_object': Column(String(64)),
    #             'update_time': Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    #         })
    #         UserAction._mapper[class_name] = ModelClass
    #
    #     cls = ModelClass()
    #     if value_dict:
    #         for k, v in value_dict.items():
    #             setattr(cls, k, v)
    #     return cls


if __name__ == '__main__':
    d = {
        'uid': 2,
        'p_type': '0',
        't_type': '1',
        'a_type': '4',
        'aimei_object': '1001',
    }
    user_action = UserAction.gen_model(d)
    user_action.session.add(user_action)
    actions = user_action.Q.all()
    print(actions)

# conn.execute(MyTable.insert(), [{'color': 'blue'},
#                                 {'color': 'red'},
#                                 {'color': 'green'}])
