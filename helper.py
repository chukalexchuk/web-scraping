import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd


def replace_spaces_with_hyphen(words):
    """Replaces space between words to hyphens"""
    return '-'.join(words.split())


def get_data_seek(url):
    """Get data: job title, company name and link from seek.cp.nz"""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("article")  # get job titles
    companies = soup.find_all("a")  # get company names

    # creating empty lists to fill with data
    title_col = []
    company_col = []
    link_col = []

    for info in titles:
        position_title = info.get('aria-label')
        title_id = info.get('data-job-id')
        title_col.append(position_title)
        link_col.append(title_id)

    for company in companies:
        company_name = company.get('aria-label')
        if type(company_name) == str:
            if company_name.startswith("Jobs at"):
                company_col.append(company_name)

    collected_data = pd.DataFrame({"Job title": title_col,
                                   "Company": company_col,
                                   "Link": link_col})
    # adding id to the url address to create working link
    collected_data['Link'] = 'https://www.seek.co.nz/job/' + collected_data['Link'].astype(str)

    return collected_data


def make_clickable(link):
    # extract clickable text to display as a link
    text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{text}</a>'

