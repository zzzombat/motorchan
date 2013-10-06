
from jsonschema import Draft4Validator

User = Draft4Validator({
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
    "additionalProperties": False,
})

Board = Draft4Validator({
    "type": "object",
    "properties": {
        "slug": {"type": "string"},
        "name": {"type": "string"},
    },
    "required": ["slug", "name"],
    "additionalProperties": False,
})

Post = Draft4Validator({
    "type": "object",
    "properties": {
        "no": {"type": "integer"},
        "board_id": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "is_sage": {"type": "boolean"},
        "parent_id": {"type": "integer"},
        "body": {"type": "string"},
    },
    "required": ["body", "board_id"],
    "additionalProperties": False,
})

Thread = Draft4Validator({
    "type": "object",
    "properties": {
        "no": {"type": "integer"},
        "board_id": {"type": "string"},
        "op": {"type": "object"},
        "replies": {"type": "array"},
    },
    "required": ["board_id", "op"]
})

# if __name__ == '__main__':
#     import ipdb;ipdb.set_trace()
