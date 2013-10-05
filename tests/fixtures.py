
import datetime

EXAMPLE_BOARDS = [{
    'name': u'B',
    'slug': u'b',
    'post_max_id': 0,
},{
    'name': u'Misc',
    'slug': u'm',
    'post_max_id': 0,
},{
    'name': u'Before Test Update',
    'slug': u'test_update',
    'post_max_id': 0,
}]

EXAMPLE_THREADS = [{
    'no': None,
    'board_id': None,
    'op': {
        'no': 12,
        'name': '',
        'email': '',
        'is_sage': False,
        'body': 'My test post',
        'date': datetime.datetime.now(),
    },
    'replies': []
}]

def setup(db):
    db.boards.insert(EXAMPLE_BOARDS)
    board = db.boards.find_one()
    for thread in EXAMPLE_THREADS:
        thread['board_id'] = board['_id']
        db.threads.insert(thread)
