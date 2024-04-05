import streamlit as st
import requests
from urllib.parse import urlencode
import pandas as pd
import datetime
import pysolr
#from urllib2 import *

# Define function to query Solr
def search_posts(query, min_upvotes=None, upvotes_sort='desc', start_date=None, end_date=None):
    # if query is empty q should be *:*
    params = {
        'q': f'(PostContent:{query} OR Post_Title:{query} OR PostComments:{query} OR CommentReply:{query})',
        'q.op': 'OR',
        'rows': 100,
        'wt': 'json'
    }
    # For testing
    url = 'http://localhost:8983/solr/crypto/select?' + urlencode(params)
    st.write("Query URL:", url)

    # Search by upvotes
    if min_upvotes is not None:
        params['fq'] = f'PostUpvotes:[{min_upvotes} TO *]'
    # Sort by upvotes
    if upvotes_sort:
        params['sort'] = f'PostUpvotes {upvotes_sort}'

    # Sort and Filer by Date
    if start_date and end_date:
        params['fq'] = f'{params.get("fq", "")} AND PostTime:[{start_date} TO {end_date}]'
    elif start_date:
        params['fq'] = f'{params.get("fq", "")} AND PostTime:[{start_date} TO *]'
    elif end_date:
        params['fq'] = f'{params.get("fq", "")} AND PostTime:[* TO {end_date}]'

    
    response = requests.get('http://localhost:8983/solr/crypto/select', params=params)
    if response.status_code == 200:
        return response.json()['response']['docs']
    else:
        return []
    
def main():
    #solr = pysolr.Solr('http://localhost:8983/solr/#/crypto', timeout=10)
    st.title("Reddit Post Search")
    text_search = st.text_input("Search Reddit posts", value="")

    # Filter and sort by upvotes
    min_upvotes = st.sidebar.number_input("Minimum Upvotes", value=0, step=1)
    sort_order_upvotes = st.sidebar.selectbox("Sort UpVotes", ["Descending", "Ascending"])
    if sort_order_upvotes == "Descending":
        upvotes_sort = 'desc'
    else:
        upvotes_sort = 'asc'

    # Filer and sort by Date
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    date_sort_order = st.sidebar.selectbox("Sort Order by Date", ["Latest", "Oldest"])
    if date_sort_order == "Latest":
        date_sort = 'desc'
    else:
        date_sort = 'asc'



    if st.button("Search"):
        # Convert date input to string format
        start_date_str = start_date.strftime('%Y-%m-%dT00:00:00Z') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%dT23:59:59Z') if end_date else None

        search_results = search_posts(text_search, min_upvotes=min_upvotes, upvotes_sort=upvotes_sort, start_date=start_date_str, end_date=end_date_str,)
        if search_results:
            df = pd.DataFrame(search_results)
            if date_sort_order == 'desc':
                df = df.sort_values(by='PostTime', ascending=False)
            else:
                df = df.sort_values(by='PostTime', ascending=True)
            st.write(df)
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()

# timeline search
# calendar or slider with numbers
# https://streamlit.io/

# enhanced search
# histogram, piechart, word cloud
# https://docs.streamlit.io/library/api-reference/charts

# search bar, when there is a query show some data belonging to a csv, maybe create bar charts and stuff
# https://blog.streamlit.io/create-a-search-engine-with-streamlit-and-google-sheets/

# another search method is a calendar

# df = pd.read_csv("combined_excel.csv")
# text_search = st.text_input("Search Reddit posts", value="")
# #date = st.date_input("Pick a date")
# date = st.date_input(
#     "Select date",
#     (datetime.date(2015, 1, 1), datetime.date(2024, 12, 1)),
#     min_value=datetime.date(2015, 1, 1), max_value=datetime.date(2024, 12, 1)
# )

# m1 = df["PostTitle"].str.contains(text_search)
# # m2 = date[0] <= datetime.date((df["Post Time"].str)[:10]) <= date[1]

# df["PostTime"] = pd.to_datetime(df["PostTime"])
# m2 = []
# for post_time in df["PostTime"]:
#     post_date = post_time.date()
#     condition_met = date[0] <= post_date <= date[1]
#     m2.append(condition_met)

# print("Calendar", str(date))

# df_search = df[m1 & m2]
# #print(df_search)

# if text_search:
#     st.write(df_search)
#     st.bar_chart(df_search, x="CommentAuthor", y="CommentUpvotes")

