def test_function(test_thing: str) -> str:
    print('yippie')
    return "yippie"

def test_function_2(test_thing: bool) -> bool:
    print('yippie2')
    return True

def test_function_3(test_thing: float) -> bool:
    print('yippie3')
    return True

def test_function_4(test_thing: str, test_thing_2: bool) -> bool:
    print('yippie4')
    return True

def test_function_5(test_thing: str, test_thing_2: bool):
    print('yippie5')
    return True

test_function("yippie")
test_function_2(True)
test_function_3(0.11)
test_function_4("yippie", True)
test_function_5("yippie", True)