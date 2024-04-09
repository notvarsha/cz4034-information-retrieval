import streamlit as st
import requests
from urllib.parse import urlencode
import pandas as pd
from datetime import datetime, timedelta
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib
import matplotlib.pyplot as plt
import seaborn
from urllib import *
from PIL import Image
import numpy as np


# To Do
# sort need choose bwt date and upvotes
# Style each reddit post nicer
# Spell check (not sure if already have) 
# More like this feature
# Add images/video using reddit url

# Define function to query Solr
def search_posts(query, selected_subreddits=["All"], min_upvotes=None, upvotes_sort='desc', start_date=None, end_date=None, date_sort='desc'):
    # if query is empty q should be *:*
    subreddit_query = ""
    if "All" not in selected_subreddits:
        subreddit_query = " OR ".join([f'Subreddit:{sub}' for sub in selected_subreddits])
    
    date_query = ""
    if start_date and end_date:
        date_query = f'PostTime:[{start_date} TO {end_date}]'
    elif start_date:
        date_query = f'PostTime:[{start_date} TO *]'
    elif end_date:
        date_query = f'PostTime:[* TO {end_date}]'
    
    main_query = f'(PostContent:{query} OR PostTitle:{query} OR PostComments:{query} OR CommentReply:{query})'

    full_query = main_query
    if subreddit_query:
        full_query += f' AND ({subreddit_query})'
    if date_query:
        full_query += f' AND ({date_query})'

    params = {
        'q': full_query,
        'q.op': 'OR',
        'rows': 1000,
        'wt': 'json'
    }

    # Search by upvotes
    if min_upvotes is not None:
        params['fq'] = f'PostUpvotes:[{min_upvotes} TO *]'
    # Sort by upvotes
    if upvotes_sort:
        params['sort'] = f'PostUpvotes {upvotes_sort}'

    if date_sort:
       params['sort'] = f'PostTime {date_sort}'
    
    # For testing
    url = 'http://localhost:8983/solr/crypto/select?' + urlencode(params)
    st.write("Query URL:", url)

    #response = requests.get('http://localhost:8983/solr/crypto/select?', params=params)
    response = requests.get(url)
    #st.write(response.status_code)

    if response.status_code == 200:
        return response.json()['response']['docs']
    else:
        return []


def main():
    st.title("Cryptocurrency Reddit Search")
    text_search = st.text_input("Input Query", value="")

    # Filter and sort by upvotes
    min_upvotes = st.sidebar.number_input("Minimum Upvotes", value=0, step=1)
    sort_order_upvotes = st.sidebar.selectbox("Sort by UpVotes", ["Descending", "Ascending"])
    if sort_order_upvotes == "Descending":
        upvotes_sort = 'desc'
    else:
        upvotes_sort = 'asc'

    # Filer and sort by Date
    default_start_date = datetime.now()
    start_date = st.sidebar.date_input("Start Date", value=default_start_date)
    end_date = st.sidebar.date_input("End Date")
    date_sort_order = st.sidebar.selectbox("Sort by Date", ["Latest", "Oldest"])
    if date_sort_order == "Latest":
        date_sort = 'desc'
    else:
        date_sort = 'asc'

    # Filter by subreddit
    subreddits = ["All", "Cryptocurrency", "CryptocurrencyNews", "CryptocurrencyMemes", "CryptoIndia", 
                  "CryptoMarkets", "CryptoMoonShots", "CryptoScams", "CryptoScamAwareness", 
                  "CryptoScamBlacklist", "CryptoScamDefence", "CryptoScammerAbuse", "CryptoScamReport", 
                  "CryptoTechnology"]
    
    selected_subreddits = st.sidebar.multiselect("Select Topics", subreddits, default="All")

    if st.button("Search"):
        # Convert date input to string format
        start_date_str = start_date.strftime('%Y-%m-%dT00:00:00Z') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%dT23:59:59Z') if end_date else None

        search_results = search_posts(text_search, selected_subreddits, min_upvotes=min_upvotes, upvotes_sort=upvotes_sort, start_date=start_date_str, end_date=end_date_str, date_sort=date_sort)
        if search_results:
            # Calculate sentiment distribution and Word Cloud
            data_analytics(search_results)

            st.write("Number of results:", len(search_results))
            # Obtain and group info and comments for each post
            grouped_comments = {}
            for result in search_results:
                post_content = str(result.get('PostContent')).strip("[]'")
                post_title = result.get('PostTitle')
                comment = result.get('PostComments')
                post_author = str(result.get('PostAuthor')).strip("[]'")  
                post_upvotes = str(result.get('PostUpvotes')).strip("[]'")
                time_str = str(result.get('PostTime')).strip("[]'")
                time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
                post_time = time_obj.strftime("%Y-%m-%d %H:%M:%S")
                subreddit = str(result.get('Subreddit')).strip("[]'")

                if isinstance(post_title, list):
                    post_title = post_title[0]
                if post_title not in grouped_comments:
                    grouped_comments[post_title] = {'author': post_author, 'content': post_content, 'subreddit':subreddit, 'upvotes': post_upvotes, 'time': post_time, 'comments': []}
                grouped_comments[post_title]['comments'].append(comment)

            # Display each post in a container
            for post_title, post_info in grouped_comments.items():
                container = st.container(border=True)
                with container:
                    # st.markdown(f"**r/:** {subreddit}")
                    # st.markdown(f"{post_info['time']}")
                    #st.markdown(f"**Post Title:** {post_title}")

                    # st.image('crypto_icon.png', width=20)
                    st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
            f"<div style='font-size: 16px; display: flex; align-items: center;'>"
            f"<img src='https://styles.redditmedia.com/t5_2wlj3/styles/communityIcon_6ddnoarvwchb1.png' style='width: 20px; height: 20px; margin-right: 5px;'/>"
            f"r/{subreddit}</div>"
            f"<div style='text-align: right; font-size: 16px;'>{post_info['time']}<br></div>"
            f"</div>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:25px'><strong>{post_title}</strong></p>", unsafe_allow_html=True)
                    st.markdown(f"{post_info['content']}")
                    st.markdown(f":arrow_up: {post_info['upvotes']} :arrow_down:")
                    # st.markdown(f"u/{post_info['author']}")

                    # Display comments in a dropdown
                    with st.expander("View Comments"):
                        for i, comment in enumerate(post_info['comments'], start=1):
                            comment_str = str(comment).strip("['']").replace("'", "")
                            if comment_str not in ['deleted', 'removed']:
                                st.markdown(f"• {comment_str}")

            # # bar chart (remove if not needed)
            # df_small = df_search[["PostID", "PostAuthor"]].drop_duplicates()
            # df_grouped = df_small.groupby(by=["PostAuthor"], as_index=False).size()
            # df_sorted = df_grouped.sort_values(by="size", ascending=False)
            # df_sorted = df_sorted.rename(columns={"PostAuthor":"Top post authors", "size":"Number of posts"})
            # st.bar_chart(df_sorted.head(10), x="Top post authors", y="Number of posts")
                    
        else:
            st.write("No results found.")

def data_analytics(search_results):
    # Sentiment Analysis
    sentiments = [result.get('sentiment') for result in search_results]
    sentiment_counts = pd.Series(sentiments).value_counts()
    labels = ['Negative', 'Neutral', 'Positive']
    sizes = [sentiment_counts[-1], sentiment_counts[0], sentiment_counts[1]]
    palette_color = seaborn.color_palette('Pastel1')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.pie(sizes, labels=labels, colors=palette_color, autopct='%1.1f%%', startangle=0)
    ax1.axis('equal')

    # Word Cloud
    text = " ".join([comment for result in search_results for comment in result.get('PostComments', [])])
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and word.isalnum()]

    mask_image = np.array(Image.open("bitcoin.png"))
    colours = matplotlib.cm.get_cmap('ocean')

    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          mask=mask_image, max_words=100, colormap=colours).generate(' '.join(tokens))
    
    ax2.imshow(wordcloud, interpolation='bilinear')
    ax2.axis('off')
    st.pyplot(fig)


if __name__ == "__main__":
    main()