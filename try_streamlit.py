import streamlit as st
import requests
from urllib.parse import urlencode
import pandas as pd
from datetime import datetime, timedelta
import pysolr
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# To Do
# Remove "deleted" comments from list before displaying
# Retrieve subreddit from URL
# Style each reddit post nicer
# Word cloud
# Spell check (not sure if already have) 
#

# Define function to query Solr
def search_posts(query, min_upvotes=None, upvotes_sort='desc', start_date=None, end_date=None, date_sort='desc'):
    # if query is empty q should be *:*
    params = {
        'q': f'(PostContent:{query} OR Post_Title:{query} OR PostComments:{query} OR CommentReply:{query})',
        'q.op': 'OR',
        'rows': 1000,
        'wt': 'json'
    }
    # For testing
    #url = 'http://localhost:8983/solr/crypto/select?' + urlencode(params)
    #st.write("Query URL:", url)

    # Search by upvotes
    if min_upvotes is not None:
        params['fq'] = f'PostUpvotes:[{min_upvotes} TO *]'
    # Sort by upvotes
    if upvotes_sort:
        params['sort'] = f'PostUpvotes {upvotes_sort}'

    # Sort and Filer by Date
    # if start_date and end_date:
    #     params['fq'] = f'{params.get("fq", "")} AND PostTime:[{start_date} TO {end_date}]'
    # elif start_date:
    #     params['fq'] = f'{params.get("fq", "")} AND PostTime:[{start_date} TO *]'
    # elif end_date:
    #     params['fq'] = f'{params.get("fq", "")} AND PostTime:[* TO {end_date}]'
    #if date_sort:
    #    params['sort'] = f'PostTime {date_sort}'

    response = requests.get('http://localhost:8983/solr/crypto/select', params=params)
    if response.status_code == 200:
        return response.json()['response']['docs']
    else:
        return []
    
def main():
    st.title("Reddit Post Search")
    text_search = st.text_input("Search Reddit posts", value="")

    # Filter and sort by upvotes
    min_upvotes = st.sidebar.number_input("Minimum Upvotes", value=0, step=1)
    sort_order_upvotes = st.sidebar.selectbox("Sort by UpVotes", ["Descending", "Ascending"])
    if sort_order_upvotes == "Descending":
        upvotes_sort = 'desc'
    else:
        upvotes_sort = 'asc'

    # Filer and sort by Date
    default_start_date = datetime.now() - timedelta(days=365*15)  # Default start date is 7 days ago
    start_date = st.sidebar.date_input("Start Date", value=default_start_date)
    end_date = st.sidebar.date_input("End Date")
    date_sort_order = st.sidebar.selectbox("Sort by Date", ["Latest", "Oldest"])
    if date_sort_order == "Latest":
        date_sort = 'desc'
    else:
        date_sort = 'asc'

    if st.button("Search"):
        # Convert date input to string format
        start_date_str = start_date.strftime('%Y-%m-%dT00:00:00Z') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%dT23:59:59Z') if end_date else None

        search_results = search_posts(text_search, min_upvotes=min_upvotes, upvotes_sort=upvotes_sort, start_date=start_date_str, end_date=end_date_str, date_sort=date_sort)

        if search_results:
            st.write("Number of results:", len(search_results))

            # Obtain and group info and comments for each post
            grouped_comments = {}
            for result in search_results:
                post_title = result.get('Post_Title')
                comment = result.get('PostComments')
                post_author = str(result.get('PostAuthor')).strip("[]'")  
                post_upvotes = str(result.get('PostUpvotes')).strip("[]'")
                post_time = str(result.get('PostTime')).strip("[]'")
                if isinstance(post_title, list):
                    post_title = post_title[0]
                if post_title not in grouped_comments:
                    grouped_comments[post_title] = {'author': post_author, 'upvotes': post_upvotes, 'time': post_time, 'comments': []}
                grouped_comments[post_title]['comments'].append(comment)

            # Display each post in a container
            for post_title, post_info in grouped_comments.items():
                container = st.container(border=True)
                with container:
                    st.markdown(f"**Post Title:** {post_title}")
                    st.markdown(f"**Author:** {post_info['author']}")
                    st.markdown(f"**Upvotes:** {post_info['upvotes']}")
                    st.markdown(f"**Time Posted:** {post_info['time']}")

                    # Display comments in a dropdown
                    with st.expander("View Comments"):
                        for i, comment in enumerate(post_info['comments'], start=1):
                            comment_str = str(comment).strip("['']").replace("'", "")
                            st.markdown(f"• {comment_str}")

            # word cloud
            df_search = pd.DataFrame(search_results)
            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(
                background_color='white',
                stopwords=stopwords,
                max_words=200,
                max_font_size=40,
                scale = 3,
                random_state=1
            ).generate(str(df_search["PostTitle"].unique())) # word cloud from post title column
            plt.axis('off')
            fig = plt.figure(1, figsize=(7, 7))
            fig.suptitle("Word Cloud", fontsize=10)
            fig.subplots_adjust(top=2.4)
            plt.imshow(wordcloud)
            st.pyplot(fig)

            # bar chart (remove if not needed)
            df_small = df_search[["PostID", "PostAuthor"]].drop_duplicates()
            df_grouped = df_small.groupby(by=["PostAuthor"], as_index=False).size()
            df_sorted = df_grouped.sort_values(by="size", ascending=False)
            df_sorted = df_sorted.rename(columns={"PostAuthor":"Top post authors", "size":"Number of posts"})
            st.bar_chart(df_sorted.head(10), x="Top post authors", y="Number of posts")
            
            # pie chart of positive, negative, neutral
        
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

