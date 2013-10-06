import string
import random
import datetime

import dateutil.tz
from bson.objectid import ObjectId

def utc_now():
    return datetime.datetime.now(dateutil.tz.tzutc())

def make_unique_board_letters_gen():
    letters = set(string.letters)
    while letters:
        yield letters.pop()

unique_board_letters = make_unique_board_letters_gen()


def make_unique_numbers_gen():
    i = 1
    while True:
        yield i
        i += 1

unique_numbers = make_unique_numbers_gen()


def get_random_string(max_len=15, use_spaces=False):
    letters = string.letters + string.digits
    if use_spaces:
        letters = " {0} ".format(letters)
    return ''.join(random.choice(letters) for x in range(max_len))


def get_random_post(name=None, email=None, parent_id=None, is_sage=False, board_id=None):
    if board_id is None:
        board_id = ObjectId()

    if name is None:
        name = get_random_string()

    if email is None:
        email = "{0}@{1}.{2}".format(
            get_random_string(5),
            get_random_string(10),
            get_random_string(2)
        )

    return {
        'no': unique_numbers.next(),
        'board_id': board_id,
        'name': name,
        'email': email,
        'is_sage': is_sage,
        'body': get_random_string(400, use_spaces=True),
        'date_created': utc_now(),
    }


def get_random_thread(board_id=None, replies_count=0):
    if board_id is None:
        board_id = ObjectId()

    replies = [get_random_post(board_id) for x in xrange(replies_count)]

    return {
        'no': unique_numbers.next(),
        'board_id': board_id,
        'op': get_random_post(),
        'replies': replies,
    }


def get_random_board(_id=None, slug=None, post_max_id=0):
    if slug is None:
        slug = unique_board_letters.next()
    if _id is None:
        _id = ObjectId()
    return {
        '_id': _id,
        'name': get_random_string(),
        'slug': slug,
        'post_max_id': post_max_id,
    }
