from index import handler


def test_handler():
    assert handler(None, None) == {"v": "1.19.5"}
