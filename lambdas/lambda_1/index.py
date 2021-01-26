from db_utils import db

def handler():
    print("Hello from Lambda 2!")
    return db()
