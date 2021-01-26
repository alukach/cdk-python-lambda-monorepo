from .index import handler

def test_handler():
    assert handler() == {'version': '1.3.22'}
