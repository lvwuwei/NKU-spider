from bs4 import BeautifulSoup as bs
import requests
import re
import time


root_url = 'http://cyber.nankai.edu.cn'
urls = [
    '/teachers/search/1',
    '/teachers/search/2',
    '/teachers/search/3',
    '/teachers/search/4'
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    response = requests.get(root_url+url, headers=headers)
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result


def find_teacher_list(url):
    response = requests.get(root_url+url, headers=headers)
    page = bs(response.text, 'html.parser')
    print(page.prettify())
    teacher_list = page.select('.accordion-right-padding td a')
    with open('teacher.txt', 'a') as f:
        for teacher in teacher_list:
            name = teacher.get_text()
            email_list = find_teacher(teacher['href'])
            email_list = list(set(email_list))
            print(name, email_list)
            # f.write(f'人工智能学院\t{name}')
            # for email in email_list:
            #     f.write(f'\t{email}')
            # f.write('\n')


for url in urls:
    find_teacher_list(url)

