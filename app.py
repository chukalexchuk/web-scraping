import pandas as pd
import streamlit as st

from geopy.geocoders import Nominatim
from helper import replace_spaces_with_hyphen, get_data_seek, make_clickable
from PIL import Image

logo_page = Image.open("logo_page.png")
image = Image.open("logo.png")
st.set_page_config(
    page_title="Data Jobs",
    page_icon=logo_page,
    layout="wide",
    menu_items={
        # 'Get Help': '', # links can be added to Readme file
        # 'Report a bug': "",
        'About': "Data Jobs"
    }
)

sidebar_image = Image.open("logo.png")
st.sidebar.image(
    sidebar_image
)
####################################################################################
# Sidebar
####################################################################################
# ask user for keywords to start the search
keywords = st.sidebar.text_input("Enter keywords for you search", value='data engineer')
# ask user to select location
location_selected = st.sidebar.selectbox("Select location", options=["New Zealand", "Wellington", "Auckland", "Christchurch"])
st.sidebar.markdown("""---""")
st.sidebar.write("This app allows to quickly check all Data Science /"
                 "Data Engineering positions from the first "
                 "10 pages of seek.co.nz")

geolocator = Nominatim(user_agent="Data Jobs")
location = geolocator.geocode(location_selected)

# get coordinates for the selected location
lat = location.latitude
lon = location.longitude

# create dataframe with coordinates
map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

# replace spaces between words
query = replace_spaces_with_hyphen(keywords)
location = replace_spaces_with_hyphen(location_selected)

# default url address for seek.co.nz website
url_page1 = f"https://www.seek.co.nz/{query}-jobs/in-All-{location}"

####################################################################################
# Main page
####################################################################################

# show the selected location on the map
st.map(map_data, zoom=5)
# create dataframe to fill with data from the 1st page
df_1st_page = get_data_seek(url_page1)

# create an empty dataframe to fill with data from other pages
df_next_pages = pd.DataFrame()

# loop for all other pages to get data
for page_num in range(2, 11):
    url_next_pages = f"https://www.seek.co.nz/{query}-jobs/in-All-{location}?page={page_num}"
    df_next_pages = pd.concat([df_next_pages, get_data_seek(url_next_pages)])

# create one dataframe with all results
df_all_jobs = pd.concat([df_1st_page, df_next_pages])

# apply make_clickable to the link column
df_all_jobs['Link'] = df_all_jobs['Link'].apply(make_clickable)

if query:
    st.write(df_all_jobs.to_html(index=False, escape=False), unsafe_allow_html=True)
