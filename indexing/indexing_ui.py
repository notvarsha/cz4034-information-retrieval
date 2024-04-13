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


# Define function to query Solr
def search_posts(query, selected_subreddits=["All"], min_upvotes=None, start_date=None, end_date=None, sort_option='Upvotes', sort='desc'):
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
    if sort_option == "Upvotes":
        params['sort'] = f'PostUpvotes {sort}'
    else:
       params['sort'] = f'PostTime {sort}'
    
    url = 'http://localhost:8983/solr/new_core/select?' + urlencode(params)
    response = requests.get(url)
    # st.write(url)

    if response.status_code == 200:
        return response.json()['response']['docs']
    else:
        return []

def spellcheck(query):
    params = {
        'q.op': 'OR',
        'q': query,
        'spellcheck': 'true',
        'wt': 'json'
    }
    url = 'http://localhost:8983/solr/new_core/spell?' + urlencode(params)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        suggestions = data['spellcheck']['suggestions']
        return [item['word'] for item in suggestions[1]['suggestion'][:5]]
    else:
        return []
    

def main():
    st.title("Cryptocurrency Reddit Search")
    text_search = st.text_input("Input Query", value="")

    # Filter and sort by upvotes and dates
    start_date = st.sidebar.date_input("Start Date", value=datetime.now())
    end_date = st.sidebar.date_input("End Date")
    sort_option = st.sidebar.selectbox("Sort by", ["Date Posted", "Upvotes"])

    if sort_option == "Date Posted":
        date_sort_order = st.sidebar.selectbox("Sort by Date Posted", ["Latest", "Oldest"])
        if date_sort_order == "Latest":
            sort = 'desc'
        else:
            sort = 'asc'
    else:
        sort_order_upvotes = st.sidebar.selectbox("Sort by Upvotes", ["Descending", "Ascending"])
        if sort_order_upvotes == "Descending":
            sort = 'desc'
        else:
            sort = 'asc'

    min_upvotes = st.sidebar.number_input("Minimum Upvotes", value=0, step=1)

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

        search_results = search_posts(text_search, selected_subreddits, min_upvotes=min_upvotes, start_date=start_date_str, end_date=end_date_str, sort_option=sort_option, sort=sort)
        # suggestions = spellcheck(text_search)

        # if suggestions and len(search_results)==0:
        #     formatted_suggestions = [f"<span style='font-weight: bold; color: red;'>{suggestion}</span>" for suggestion in suggestions]
        #     st.markdown("Did you mean: " + ", ".join(formatted_suggestions), unsafe_allow_html=True)

        if search_results:
            tab1, tab2 = st.tabs(["Results :mag:", "Stats :bar_chart:"])

            with tab2:
                # Calculate sentiment distribution and Word Cloud
                data_analytics(search_results)
            
            # Obtain and group info and comments for each post
            grouped_comments = {}
            for result in search_results:
                post_content = str(result.get('PostContent')).strip("['']").replace('"', '')
                post_title = result.get('PostTitle')
                comment = result.get('PostComments')
                post_author = str(result.get('PostAuthor')).strip("[]'")  
                post_upvotes = str(result.get('PostUpvotes')).strip("[]'")
                time_str = str(result.get('PostTime')).strip("[]'")
                time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
                post_time = time_obj.strftime("%Y-%m-%d %H:%M:%S")
                subreddit = str(result.get('Subreddit')).strip("[]'")

                if post_author!='jonbristow':
                    if isinstance(post_title, list):
                        post_title = post_title[0]
                    if post_title not in grouped_comments:
                            grouped_comments[post_title] = {'author': post_author, 'content': post_content, 'subreddit':subreddit, 'upvotes': post_upvotes, 'time': post_time, 'comments': []}
                    grouped_comments[post_title]['comments'].append(comment)

            with tab1:
                st.write("Number of results:", len(search_results))
                # Display each post in a container
                for post_title, post_info in grouped_comments.items():
                    container = st.container(border=True)
                    with container:
                        st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
                                    f"<div style='font-size: 16px; display: flex; align-items: center;'>"
                                    f"<img src='https://styles.redditmedia.com/t5_2wlj3/styles/communityIcon_6ddnoarvwchb1.png' style='width: 20px; height: 20px; margin-right: 5px;'/>"
                                    f"r/{subreddit}</div>"
                                    f"<div style='text-align: right; font-size: 16px;'>{post_info['time']}<br></div>"
                                    f"</div>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size:25px'><strong>{post_title}</strong></p>", unsafe_allow_html=True)

                        # Display Video, Image or Text
                        if post_info['content'].startswith('https://v.redd.it/'):
                            st.video(post_info['content'])
                        elif post_info['content'].startswith('https://i.redd.it/'):
                            st.image(post_info['content'])
                        else:
                            st.markdown(f"{post_info['content']}")
                            
                        st.markdown(f":small_red_triangle: {post_info['upvotes']} :small_red_triangle_down:")

                        # Display comments in a dropdown
                        with st.expander("View Comments"):
                            for i, comment in enumerate(post_info['comments'], start=1):
                                comment_str = str(comment).strip("['']").replace('"', '')
                                if comment_str not in ['deleted', 'removed']:
                                    st.markdown(f"• {comment_str}")
        else:
            st.write("No results found.")

        


def data_analytics(search_results):
    # Sentiment Analysis
    sentiments = [result.get('Sentiment') for result in search_results]
    sentiment_counts = pd.Series(sentiments).value_counts()
    labels = ['Negative', 'Neutral', 'Positive']
    sizes = [
    sentiment_counts.get(-1, 0),  # Negative sentiment, default to 0 if not found
    sentiment_counts.get(0, 0),   # Neutral sentiment, default to 0 if not found
    sentiment_counts.get(1, 0)    # Positive sentiment, default to 0 if not found
    ]
    filtered_labels = [label for label, count in zip(labels, sizes) if count > 0]
    filtered_sizes = [size for size in sizes if size > 0]
    
    palette_color = seaborn.color_palette('Pastel1')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.pie(filtered_sizes, labels=filtered_labels, colors=palette_color, autopct='%1.1f%%', startangle=0)
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