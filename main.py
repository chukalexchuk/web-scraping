import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

####################################################################################
# Sidebar
####################################################################################
# Test version!!!!! working not with all keywords!!!!!
# ask user for keywords to start the search
st.sidebar.info("This app allows to quickly check all positions from the first 10 pages of seek.co.nz")
keywords = st.sidebar.text_input("Please enter keywords for you search", value='data engineer')


def replace_spaces_with_hyphen(words):
    """Replaces space between words to hyphens"""
    return '-'.join(words.split())


query = replace_spaces_with_hyphen(keywords)
# default url address for seek.co.nz website
url_page1 = (f"https://www.seek.co.nz/{query}-jobs")


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


# create dataframe to fill with data from the 1st page
df_1st_page = get_data_seek(url_page1)

# create an empty dataframe to fill with data from other pages
df_next_pages = pd.DataFrame()

# loop for all other pages to get data
for page_num in range(2, 11):
    url_next_pages = (f"https://www.seek.co.nz/{query}-jobs?page={page_num}")
    df_next_pages = pd.concat([df_next_pages, get_data_seek(url_next_pages)])

# create one dataframe with all results
df_all_jobs = pd.concat([df_1st_page, df_next_pages])


def make_clickable(link):
    # extract clickable text to display as a link
    text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{text}</a>'


# apply make_clickable to the link column
df_all_jobs['Link'] = df_all_jobs['Link'].apply(make_clickable)

if query:
    st.write(df_all_jobs.to_html(escape=False), unsafe_allow_html=True)
