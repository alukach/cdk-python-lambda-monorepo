from db_utils import db


def handler(event, context):
    print("Hello from Lambda 1!")
    return db()
