import requests
from io import StringIO
from lxml import html
from lxml.etree import HTMLParser, parse, tostring


def get_hml_content(url:str = 'https://example.com') -> str:
    """ Get html from source """
    response = requests.get(url)
    return response.text


def get_tree(html_text:str):
    return html.fromstring(html_text)


def find_by(tree, locator, by_text=True):
    if by_text:
        return tree.findtext(locator)
    else:
        return tree.xpath(locator)


broken_html = """<html><head>
<title>test<body><h1>page title</h1>
<a href='mailto:my@mail.com' rel='my@mail.com'>click me</a>
<p class='abc' > some text
<div id="xyz"> text </div>  <p class="">невірний, покоцаний html
""" # невірний покоцаний хтмл


def clean_html(broken_html:str):
    tree = parse(StringIO(broken_html), HTMLParser(encoding="utf8"))
    result = tostring(tree.getroot(),
                      pretty_print=True,
                      method="html")
    return result.decode("utf-8")


if __name__ == "__main__":
    html_content = get_hml_content()
    print(html_content)
    tree = get_tree(html_content)
    title = find_by(tree, './/title')
    print("Заголовок сторінки:", title)
    link = find_by(tree, './/a/@href', False)
    print("Посилання", link)
    clean = clean_html(broken_html)
    print(clean)
