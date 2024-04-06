# FOR TESTING QUERY RESULTS IN A DATAFRAME FORMAT

import streamlit as st
import requests
from urllib.parse import urlencode
import pandas as pd
import datetime
import pysolr

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
    min_upvotes = st.number_input("Minimum Upvotes", value=0, step=1)
    sort_order_upvotes = st.selectbox("Sort UpVotes", ["Descending", "Ascending"])
    if sort_order_upvotes == "Descending":
        upvotes_sort = 'desc'
    else:
        upvotes_sort = 'asc'

    # Filer and sort by Date
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    date_sort_order = st.selectbox("Sort Order by Date", ["Latest", "Oldest"])
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