# the main grbr app
# to run this app, run the following command in the terminal
# streamlit run app.py

import os
import requests
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup
from gsearch import search
import streamlit as st
import pandas as pd
from stqdm import stqdm
from sentence_transformers import SentenceTransformer, util
from transformers import BertTokenizerFast, EncoderDecoderModel
import torch

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

# cache the sentence transformer model
@st.cache_resource()
def get_sentence_transformer_model():
    return SentenceTransformer("ConGen-BERT-Tiny")

# cache the text summarizer model
@st.cache_resource()
def get_text_summarizer_model_and_transformer():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_endpoint = "bert-mini2bert-mini-finetuned-cnn_daily_mail-summarization"
    tokenizer = BertTokenizerFast.from_pretrained(model_endpoint)
    model = EncoderDecoderModel.from_pretrained(model_endpoint).to(device)
    
    return model, tokenizer

# create the generate summary function
def generate_summary(text, model, tokenizer):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # cut off at BERT max length 512
    inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    output = model.generate(input_ids, attention_mask=attention_mask)

    return tokenizer.decode(output[0], skip_special_tokens=True)


# @st.cache_data(ttl=60 * 60 * 24)
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


# main grbr app
st.title("GRBR - a links and summary generator tool")
st.write("GRBR is a tool that generates links and summaries for a given query term.")
# st.write("GRBR is a tool that generates links and summaries for a given RSS feed.")
# input_term = st.text_input("Enter your google alert RSS feed here:")
input_term = st.text_input("Enter your query term here:")
if input_term:
    response = search(query_term=input_term)
    # st.write(f"Here are the top 5 links for '{input_term}':")

    all_df = pd.DataFrame()
    for i in stqdm(range(10)):
        html_doc = requests.get(response[i]["link"]).text
        soup = BeautifulSoup(html_doc, "html.parser")
        p_string = " ".join([x.get_text() for x in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p"])])
        cleaned_body = "".join(
            [
                p
                for p in p_string
                if p.isalnum()
                or p.isspace()
                or p in [".", ",", "!", "?", ":", ";", "'", '"', "(", ")"]
            ]
        )
        
        ts_model, ts_tokenizer = get_text_summarizer_model_and_transformer()
        summary = generate_summary(cleaned_body, ts_model, ts_tokenizer)
        
        sentences = [input_term, summary]
        st_model = get_sentence_transformer_model()
        embeddings = st_model.encode(sentences)
        
        cos_sim = round(util.cos_sim(embeddings[0], embeddings[1]).item(), 4)
    
        all_df = pd.concat([all_df, pd.DataFrame(
            {
                "title": [response[i]["title"]],
                "semantic_similarity": [cos_sim],
                "summary": [summary],
                "link": [response[i]["link"]],
            }
        )])

    df_to_show = (all_df
                #   .assign(**{"summary_length": all_df.summary.str.len()})
                #   .loc[lambda x: x.summary_length > 20]
                #   .drop("summary_length", axis=1)
                  .drop_duplicates(subset=['summary'])
                  .sort_values(by="semantic_similarity", ascending=False)
                  .reset_index(drop=True)
                #   .head(5)
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