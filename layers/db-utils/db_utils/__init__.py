import sqlalchemy


def db():
    return {"v": sqlalchemy.__version__}
