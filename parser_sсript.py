import atexit
import json
import os

import requests
from bs4 import BeautifulSoup


# The class for processing a json file
class JSON:
    def __init__(self, filename):
        self.handler = open(filename, 'w+', encoding="utf-8")
        atexit.register(self.close)

    def save(self, data):
        text = json.dumps(data, ensure_ascii=False)
        self.handler.seek(0)
        self.handler.truncate()
        self.handler.write(text)

    def close(self):
        self.handler.close()


def clean_record(record):
    keys = ['uid', 'phone', 'fio']  # required fields from records
    data = {}
    for key_index, key in enumerate(keys):
        # clearing unnecessary information in the field
        now_render_field = record[key_index]
        now_render_field = now_render_field.replace("<span>", "").replace("</span>", "").replace("\n", "").replace(
            "&quot;",
            '"')
        now_render_field = now_render_field.strip(' ')
        data[key] = now_render_field
    return data

def main():
    url_login = os.getenv("URL_LOGIN")
    url_data = os.getenv("URL_DATA")

    json_data_path = './data.json'

    # Getting csrf for authorization
    client = requests.session()
    html_login = client.get(url_login)
    page_login = BeautifulSoup(html_login.text, 'lxml')
    login_csrf = page_login.find('meta', dict(name='csrf-token'))['content']

    # Authorization data package
    login_data = {
        '_token': login_csrf,
        'email': os.getenv("EMAIL"),
        'password': os.getenv("PASSWORD")
    }
    # Authorization request header
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'enot.lima.net.ua',
        'Origin': os.getenv("MAIN_URL"),
        'Referer': os.getenv("MAIN_URL") + '/admin/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 '
                      'YaBrowser/21.3.1.81 Yowser/2.5 Safari/537.36'
    }

    # Sending an authorization request
    log_in = client.post(url_login, data=login_data, headers=headers)

    # Getting a database authorization token
    page_data = BeautifulSoup(log_in.text, 'lxml')
    headers["X-CSRF-TOKEN"] = page_data.find('meta', dict(name='csrf-token'))["content"]

    # Request to get data from the database
    number_of_reg = -1  # if -1 return all items
    base_connection = client.post(url_data, cookies=log_in.cookies.get_dict(),
                                  data="draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D="
                                       "true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%"
                                       "5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&column"
                                       "s%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D"
                                       "%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns"
                                       "%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&c"
                                       "olumns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5"
                                       "B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3"
                                       "%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5"
                                       "Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearc"
                                       "hable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&col"
                                       "umns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5"
                                       "D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5B"
                                       "search%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D="
                                       "6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%"
                                       "5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&"
                                       "columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&co"
                                       "lumns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bs"
                                       "earch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%"
                                       "5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bva"
                                       "lue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%"
                                       "5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&colum"
                                       "ns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%"
                                       "5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B1"
                                       "0%5D%5Borderable%5D=false&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%"
                                       f"5D%5Bregex%5D=false&start=0&length={number_of_reg}&search%5Bvalue%5D=&search%5Bregex%5D=false",
                                  headers=headers)
    received_data = base_connection.json()['data']

    Json_file = JSON(json_data_path)

    finish_list = {}
    for record in received_data:
        # processing of received records

        data = clean_record(record)
        uid = data.pop('uid')
        finish_list[uid] = data

    Json_file.save(finish_list)
    Json_file.close()

if __name__ == "__main__":
    main()