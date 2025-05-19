import pytest

def count(a, b):
    return a + b

@pytest.mark.smoke
def test_count():
    actual_result = count(1, 2)
    expected_result = 3
    assert actual_result == expected_result, f"Wrong data! actual_result: {actual_result} expected_result:{expected_result}"


def test_just_test():
    assert True


def test_example():
    x = 5
    y = 10
    if x + y != 11:
        pytest.fail("Помилка: Сума x та y не дорівнює 11")
    
@pytest.mark.xfail
def test_div():
    a = 2 / 0
    # assert True

@pytest.mark.skip(reason="Причина пропуску тесту")
def test_for_skip():
    pass

def should_skip():
    # os.name == "nt" # значить стоїть вінд
    return True  # Умова, за якої потрібно пропустити тест, наприкл. тест лише для linux 

@pytest.mark.skipif(should_skip(), reason="Unsupported OS")
def test_skip_if():
    assert True


def divide(x, y):
    if y == 0:
        raise ValueError("Ділення на нуль неможливе")
    return x / y


def test_divide_by_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert str(exc_info.value) == "Ділення на нуль неможливе"
