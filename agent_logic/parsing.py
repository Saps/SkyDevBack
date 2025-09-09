
#def run(in_params={query: str, keywords: str, folder_path: str, vacancy_txt_file: str}):
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import sys
from deepseek_python_similarity_metrics import TextNormalizer, TextSimilarityCalculator
from selenium.webdriver.common.by import By
from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions


def get_cvs(keywords):  # функция парсинга и сохранения резюме в нужную папку

    text = '+'.join(keywords).replace('+ ', '+')

    pg = f'https://hh.ru/search/resume?text={text}&logic=normal&pos=full_text&exp_period=all_time&exp_company_size=any&filter_exp_period=all_time&area=1&relocation=living_or_relocation&age_from=&age_to=&gender=unknown&salary_from=&salary_to=&currency_code=RUR&order_by=relevance&search_period=0&items_on_page=1000&hhtmFrom=resume_search_form'
    records_fetched = 0

    if os.getenv('IS_WINDOWS'):
        browser = webdriver.Firefox()
    else:
        geckodriver_path = "/snap/bin/geckodriver"
        driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        browser = webdriver.Firefox(options=opts, service=driver_service)

    #browser = webdriver.Firefox(service=driver_service)

    #browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    #browser = webdriver.Firefox()
    browser.get(pg)
    soup = BeautifulSoup(browser.page_source, "lxml")

    result = []

    for a in soup.find_all("a", attrs={"data-qa": "serp-item__title"}):
        res = f"https://hh.ru{a.attrs['href'].split('?')[0]}"
        browser.get(res)
        page_text = browser.find_element(By.TAG_NAME, "body").text

        el = {
            'hyperlink' : a.attrs['href'].split('?')[0],
            'rawtext' : page_text
        }

        result.append(el)
        if len(result) > 10:
            break

    return result  # найденные записи


def run(in_params):

    #pg=''
    #browser = webdriver.Firefox()
    #browser.get(pg)

    keywords = in_params['keywords'] #ключевые слова из описания вакансии
    query = in_params['query'] #название вакансии

    keywords = keywords.split(',')
    keywords.append(query)

    records = get_cvs(keywords)
    return records