import pandas as pd
import streamlit as st
from helper import replace_spaces_with_hyphen, get_data_seek, make_clickable

####################################################################################
# Sidebar
####################################################################################
# Test version!!!!! working not with all keywords!!!!!
# ask user for keywords to start the search
st.sidebar.info("This app allows to quickly check all positions from the first 10 pages of seek.co.nz")
keywords = st.sidebar.text_input("Please enter keywords for you search", value='data engineer')

query = replace_spaces_with_hyphen(keywords)
# default url address for seek.co.nz website
url_page1 = (f"https://www.seek.co.nz/{query}-jobs")

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

# apply make_clickable to the link column
df_all_jobs['Link'] = df_all_jobs['Link'].apply(make_clickable)

if query:
    st.write(df_all_jobs.to_html(escape=False), unsafe_allow_html=True)
