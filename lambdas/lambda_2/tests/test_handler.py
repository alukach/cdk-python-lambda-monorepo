from lambda_2 import handler

def test_handler():
    assert handler() == {'data': 'asdf'}
