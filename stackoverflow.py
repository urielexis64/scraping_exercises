import requests
from bs4 import BeautifulSoup

url = "https://www.stackoverflow.com/questions"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features="lxml")

questions_container = soup.find(id="questions")
questions_list = questions_container.find_all('div', class_="question-summary")

for question in questions_list:
    question_text_tag = question.find('h3')
    question_text = question_text_tag.text

    question_desc = question_text_tag.find_next_sibling().text
    question_desc = question_desc.replace('\n', '').replace('\r', '').strip()
    print(f"Title: {question_text}")
    print(f"Desc: {question_desc}", end='\n\n')