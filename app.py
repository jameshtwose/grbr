# the main grbr app
# to run this app, run the following command in the terminal
# streamlit run app.py

import os
import requests
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup
import openai
from gsearch import search
import streamlit as st
import pandas as pd
from stqdm import stqdm

_ = load_dotenv(find_dotenv())

# configure the page
st.set_page_config(page_title="GRBR App", page_icon=":sparkles:")

# HIDE STREAMLIT STYLE
hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# @st.cache_data(ttl=60 * 60 * 24)
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


openai.api_key = os.environ.get("OPENAI_API_KEY")

# main grbr app
st.title("GRBR - a links and summary generator tool")
st.write("GRBR is a tool that generates links and summaries for a given query term.")
input_term = st.text_input("Enter your query term here:")
if input_term:
    response = search(query_term=input_term)
    st.write(f"Here are the top 5 links for '{input_term}':")

    all_df = pd.DataFrame()
    for i in stqdm(range(10)):
        html_doc = requests.get(response[0]["link"]).text
        soup = BeautifulSoup(html_doc, "html.parser")
        p_string = " ".join([x.get_text() for x in soup.find_all("p")])
        cleaned_body = "".join(
            [
                p
                for p in p_string
                if p.isalnum()
                or p.isspace()
                or p in [".", ",", "!", "?", ":", ";", "'", '"', "(", ")"]
            ]
        )
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{cleaned_body}\n\nTl;dr",
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1,
            stop=["\n"],
        )

        all_df = pd.concat([all_df, pd.DataFrame(
            {
                "title": [response[i]["title"]],
                "summary": f'{[completion["choices"][0]["text"]]}...',
                "link": [response[i]["link"]],
            }
        )])

    df_to_show = (all_df
                  .assign(**{"summary_length": all_df.summary.str.len()})
                  .loc[lambda x: x.summary_length > 20]
                  .drop("summary_length", axis=1)
                  .drop_duplicates(subset=['summary'])
                  .reset_index(drop=True)
                  .head(5)
                  )

    st.write(df_to_show)

query_reformat = "".join(
    [x for x in input_term.lower() if x.isalnum() or x.isspace()]
).replace(" ", "_")

csv = convert_df(all_df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f"grbr_{query_reformat}.csv",
    mime="text/csv",
)

st.markdown(
    """
    <div style="text-align: center; padding-right: 10px; padding-top: 20px;">
        <img alt="logo" src="https://services.jms.rocks/img/logo.png" width="100">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="text-align: center; color: #E8C003; margin-top: 40px; margin-bottom: 40px;">
        <a href="https://services.jms.rocks" style="color: #E8C003;">Created by James Twose</a>
    </div>
    """,
    unsafe_allow_html=True,
)