import streamlit as st
import pandas as pd
import datetime
# timeline search
# calendar or slider with numbers
# https://streamlit.io/

# enhanced search
# histogram, piechart, word cloud
# https://docs.streamlit.io/library/api-reference/charts

# search bar, when there is a query show some data belonging to a csv, maybe create bar charts and stuff
# https://blog.streamlit.io/create-a-search-engine-with-streamlit-and-google-sheets/

# another search method is a calendar

df = pd.read_csv("crypto.csv")
text_search = st.text_input("Search Reddit posts", value="")
#date = st.date_input("Pick a date")
date = st.date_input(
    "Select date",
    (datetime.date(2015, 1, 1), datetime.date(2024, 12, 1)),
    min_value=datetime.date(2015, 1, 1), max_value=datetime.date(2024, 12, 1)
)

m1 = df["Post Title"].str.contains(text_search)
# m2 = date[0] <= datetime.date((df["Post Time"].str)[:10]) <= date[1]

df["Post Time"] = pd.to_datetime(df["Post Time"])
m2 = []
for post_time in df["Post Time"]:
    post_date = post_time.date()
    condition_met = date[0] <= post_date <= date[1]
    m2.append(condition_met)

print("Calendar", str(date))

df_search = df[m1 & m2]
#print(df_search)

if text_search:
    st.write(df_search)
    st.bar_chart(df_search, x="Comment Author", y="Comment Upvotes")