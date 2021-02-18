import numpy


def handler(event, context):
    print("Hello from Lambda 2!")
    return {"v": numpy.__version__}
