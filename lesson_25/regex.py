import re

text1 = "Телефонний номер: (123) 456-7890"
text2 = "Телефонний номер: (123) 456-78-90"
text3 = "Телефонний номер: (123)456-78-90"

pattern_0 = r"\(\d{3}\)\s\d{3}-\d{4}"
pattern = r"\(\d{3}\)\s?\d{3}-?\d{2}-?\d{2}"

def find_by_reg(*texts, pattern=pattern):
    for t in texts:
        match = re.search(pattern, t)
        if match:
            phone_number = match.group()
            print("Знайдено номер телефону:", phone_number)

find_by_reg(text1, text2, text3)
