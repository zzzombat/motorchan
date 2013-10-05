
from pymongo import MongoClient
from tornado.options import options
from application import Application

EXAMPLE_BOARDS = [{
    'name': u'B',
    'slug': u'b',
    'post_max_id': 0,
},{
    'name': u'Misc',
    'slug': u'm',
    'post_max_id': 0,
},{
    'name': u'XYNTA',
    'slug': u'x',
    'post_max_id': 0,
}]

def main():

    db = MongoClient(options.dburl)[options.dbname]
    adminuser = db.users.find_one({"username":"admin"})
    if adminuser is None:
        db.users.insert({'username': 'admin', 'password': '1234'})

    if not db.boards.find_one():
        db.boards.insert(EXAMPLE_BOARDS)

