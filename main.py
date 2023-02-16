import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
from pprint import pprint
import json


def get_headers():
    return Headers(browser="chrome", os="win").generate()

if __name__ == '__main__':
    id_ = 1
    el = 0
    namber_all = 0
    list_all = []
    a = 0
    p = 0
    info_list = []
    while el <= namber_all:
        listing = []
        HOST = r"https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=Python&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience doesNotMatter&order_by=relevance&search_period=1&items_on_page=20&page="
        head_main_html = requests.get(f"{HOST}{el}", headers=get_headers()).text
        soup = BeautifulSoup(head_main_html, features="html.parser")
        vak_list = soup.find_all('div', class_="serp-item")
        vak_namber = soup.find_all('span', class_="pager-item-not-in-short-range")
        a = 0
        counter = 0
        # print(namber_all)
        for i_namber in vak_namber:
            a = a+1
            if a == 4 and p == 0:
                namber_page = i_namber.text # количество всего страниц на сайте
                namber_all = int(namber_page)
                print( f"Всего страниц на сайте: {namber_all}")
                p = p+1
        for tag in vak_list:
            link = tag.find('a', class_="serp-item__title")['href'] # ссылка на вакансию
            tag_specialist = tag.find(class_="serp-item__title").text #
            text = re.sub(r'\([^()]*\)', '', tag_specialist)
            tag_specialist_1 = text.lower()
            tag_specialist_choice_1 = tag_specialist_1.split()

            description = tag.find(class_="vacancy-serp-item__layout")
            description_info = description.find(class_="g-user-content")
            pattern_1 = r"Django?"
            result_1 = re.findall(pattern_1, str(description_info), re.I)
            result_choice_1 = result_1
            pattern_2 = r"Flask?"
            result_2 = re.findall(pattern_2, str(description_info), re.I)
            result_choice_2 = result_2
            if result_choice_1 != [] or result_choice_2 != [] and counter == 0:
                counter += 1
                for i in tag_specialist_choice_1:
                    tag_salary = tag.find(class_="vacancy-serp-item-body__main-info") # зарплата
                    organization = tag.find(class_="bloko-v-spacing-container bloko-v-spacing-container_base-2").text  # название организации
                    city = tag.select_one('.bloko-text[data-qa=vacancy-serp__vacancy-address]').text
                    salary = "Зарплата не указана"
                    for tag_new in tag_salary: # обработка текста зарплата
                        tag_new_1 = tag_new.find_all('span', class_='bloko-header-section-3')  # стоимость обучения в строке
                        tag_new_2 = str(tag_new_1)
                        tag_new_split = tag_new_2.split()
                        tag_clean = []
                        if tag_new_split[2:] != tag_clean:
                            tag_new_split_1 = tag_new_split[2:]
                            tag_new_split_2 = ''.join(tag_new_split_1)
                            tag_new_split_3 = list(tag_new_split_2[45:-8])
                            tag_new_split_4 = ''.join(tag_new_split_3)
                            pattern = r"(\w+)"
                            result = re.findall(pattern, tag_new_split_4)
                            tag_list = ' '.join(result)
                            if result[0] != 'от' and result[0] != 'до':
                                tag_list_1 = '-'.join(result[0:2])
                                tag_list_2 = result[2]
                                salary = ' '.join([tag_list_1, tag_list_2])
                                # print(salary)
                            elif result[0] == 'до' or result[0] == 'от':
                                salary = ' '.join(result[0:3])
                info_list.append( {id_:{"Ссылка": link,
                                 "Зарплата": salary,
                                 "Специалист": tag_specialist.replace(u"\xa0", " "),
                                 "Город": city.replace(u"\xa0", " "),
                                 "Название компании": organization.replace(u"\xa0", " "),
                                 "Номер страницы на сайте": el}})
                id_ += 1
            else:
                counter += 1
        el = el+1
        print("Обработана страница № " f"{el}" )
    print()
    print("*" * 150)
    print("Все страницы обработаны успешно")
    print(f"Всего вакансий: {id_-1}")
    pprint(info_list)
    with open(r"info.json", 'w', encoding='utf-8') as f:
        json.dump(info_list, f, ensure_ascii=False, indent=2)
