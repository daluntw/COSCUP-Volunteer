from pymongo.collection import ReturnDocument

from models.base import DBBase


class TeamDB(DBBase):
    ''' Team Collection

    :Struct:
        - ``pid``: from project id
        - ``tid``: team id
        - ``name``: team name
        - ``owners``: (list) owners for team admin
        - ``chiefs``: (list) team chiefs
        - ``members``: (list) team members

    '''
    def __init__(self, pid, tid):
        super(TeamDB, self).__init__('team')
        self.pid = pid
        self.tid = tid

    def index(self):
        ''' Index '''
        self.create_index([('pid', 1), ])

    def default(self):
        ''' default data '''
        r = {
            'pid': self.pid,
            'tid': self.tid,
            'name': '',
            'owners': [],
            'chiefs': [],
            'members': [],
        }
        self.make_create_at(r)
        return r

    def add(self, data):
        ''' Add data

        :param dict data: data

        '''
        return self.find_one_and_update(
            {'pid': self.pid, 'tid': self.tid},
            {'$set': data},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

    def update_users(self, field, add_uids, del_uids):
        ''' Update users

        :param str field: field name
        :param list add_uids: add uids
        :param list del_uids: del uids

        '''
        if add_uids is None:
            add_uids = []

        if del_uids is None:
            del_uids = []

        data = self.find_one({'pid': self.pid, 'tid': self.tid}, {field: 1})
        values = list(set(data[field]) | set(add_uids) - set(del_uids))

        self.find_one_and_update({'pid': self.pid, 'tid': self.tid}, {'$set': {field: values}})

    def get(self):
        ''' Get data '''
        return self.find_one({'pid': self.pid, 'tid': self.tid})