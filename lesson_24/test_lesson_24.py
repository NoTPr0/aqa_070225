import pytest
import requests

# Приклад тесту, який використовує фікстуру
def test_using_fixture(my_fix):
    # my_fixture - це аргумент, що передається в тестову функцію
    assert "key" in my_fix
    assert my_fix["key"] == "value"

# Приклад використання фікстури у тесті
def test_using_fixture(my_fixture):
    print(f"Test with fixture value: {my_fixture}")
    assert my_fixture % 2 == 0

# Тестова функція
def test_http_methods(http_method):
    url = "https://httpbin.org/" 
    url = url + "/get" if http_method == requests.get else url + "/post"
    data = {"example": "data"}
    if http_method == requests.get:
        response = http_method(url, params=data)
    else:
        response = http_method(url, data=data)

    assert response.status_code == 200
    json_data = response.json()

    if http_method == requests.get:
        assert json_data["args"] == data
    else:
        assert json_data["form"] == data


@pytest.mark.usefixtures("prepare_config") # більший скоуп (модуль) - дії не має
class TestClass:
    def test_1(self, prepare_database, tmpdir): # викликай ф-тури тут
        # copy file to 
        file_path = tmpdir.join("test_file.txt")
        # Запис даних у створений файл
        file_path.write("Test data")
        # Перевірка, чи файл був створений та містить правильні дані
        assert file_path.isfile()
        assert file_path.read() == "Test data"
    
    def test_2(self): # якщо викликати ф-туру тут то вона не на весь клас
        assert True
    
    def test_3(self):
        assert True

    def test_4(self):
        assert True

# Використання фікстур з conftest.py на рівні класу.
@pytest.mark.usefixtures("prepare_database", "prepare_config")
class TestClassWithMultipleFixtures:
    def test_method1(self):
        print("Тестування методу 1...")

    def test_method2(self):
        print("Тестування методу 2...")


def test_addition(input_data):
    x, y = input_data
    result = x + y
    assert result == x + y

def add(x, y):
    return x + y

@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -5, 5)
])
def test_addition(x, y, expected):
    result = add(x, y)
    assert result == expected

# Параметризований тест з використанням фікстури та параметра indirect
@pytest.mark.parametrize("prepare_data", [1, 2, 3], indirect=True)
def test_example(prepare_data):
    print(prepare_data)
    assert prepare_data % 2 == 0

