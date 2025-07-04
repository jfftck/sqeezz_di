import sqeezz

sqeezz.builder()\
.lazy_add_ref('os')


def example(test_str: str):
    print(sqeezz.using('os'), test_str, sep=' |>> ')


example('hello')

sqeezz.builder('test os')\
.add_named_ref('os', 'mocked os')

test = sqeezz.group('test os', example)
test('testing group')

example('goodbye')
