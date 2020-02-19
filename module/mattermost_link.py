from time import time
from uuid import uuid4

import setting
from models.mattermost_link_db import MattermostLinkDB


class MattermostLink(object):
    ''' MattermostLink '''
    def __init__(self, uid):
        self.uid = uid
        self.raw = MattermostLinkDB().find_one({'_id': uid})

        if not self.raw:
            mml_db = MattermostLinkDB()
            mml_db.insert_one({'_id': uid, 'code': uuid4().hex})
            self.raw = mml_db.find_one({'_id': uid})

    @classmethod
    def verify_save(cls, data):
        ''' verify and save data '''
        if 'token' in data and data['token'] == setting.MATTERMOST_SLASH_VOLUNTEER:
            if 'text' in data and data['text']:
                texts = data['text'].split(' ')
                if len(texts) < 2:
                    return False

                cmd, pwd = texts

                if cmd == 'verify':
                    uid, code = pwd.split('.')
                    mml = cls(uid=uid)
                    if code == mml.raw['code']:
                        MattermostLinkDB().find_one_and_update({'_id': uid}, {'$set': {'data': data, 'create_at': time()}})
                        return True

        return False

    @staticmethod
    def reset(uid):
        MattermostLinkDB().delete_one({'_id': uid})
