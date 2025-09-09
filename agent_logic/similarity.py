
#def run(in_params={query: str, keywords: str, folder_path: str, vacancy_txt_file: str}):
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import sys

import agent_logic.src.simularity_logic.hard_skills_similarity as hss
from deepseek_python_similarity_metrics import TextNormalizer, TextSimilarityCalculator
from selenium.webdriver.common.by import By
from selenium import webdriver


def get_similarity(vacancy_txt, resume_txt):  # считаем релевантность
    sim_dict = {}
    calculator = TextSimilarityCalculator()
    sim_hard = hss.get_similarity_by_hard_skills(resume_txt)
    sim_dict['hard'] = sim_hard['choices'][0]['message']['content']
    similarity = calculator.calculate_similarity(vacancy_txt, resume_txt)
    sim_dict['res'] = similarity
    analysis = calculator.get_detailed_analysis(vacancy_txt, resume_txt)
    sim_dict['detail'] = analysis
    return sim_dict

def run(in_params):
    sim_dict = get_similarity(in_params['vacancy_txt'], in_params['resume_txt'])
    return sim_dict