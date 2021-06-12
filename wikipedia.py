import requests

from lxml import html

url = "https://www.wikipedia.org"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

response = requests.get(url, headers=headers)

parser = html.fromstring(response.text)

# Using XPATH

# languages = parser.xpath("//a[starts-with(@id, 'js-link-box-')]/strong/text()")
#
# for lang in languages:
#     print(lang)

# Using CLASS ATTR

languages = parser.find_class('central-featured-lang')
for lang in languages:
    print(lang.text_content())