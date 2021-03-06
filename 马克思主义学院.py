from bs4 import BeautifulSoup as bs
import requests
import re


root_url = 'http://cz.nankai.edu.cn/Pages/'
urls = [
    'TeacherTeam.aspx'
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
    teacher_list = page.select('.personCard')
    with open('teacher.txt', 'a') as f:
        for teacher in teacher_list:
            name = teacher.select_one('td a').get_text()
            email_list = find_teacher(teacher.select_one('td a')['href'])
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'马克思主义学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)
