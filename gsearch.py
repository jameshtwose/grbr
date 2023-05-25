# %%
import os
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup

# %%
_ = load_dotenv(find_dotenv())


# %%
def search(query_term="lectures"):
    service = build("customsearch", "v1", developerKey=os.environ.get("GOOGLE_API_KEY"))
    res = (
        service.cse()
        .list(
            q=query_term,
            cx=os.environ.get("GOOGLE_CSE_ID"),
        )
        .execute()
    )
    return res["items"]


# %%
response = search(query_term="what are the latest innovations in sustainable plastics market?")
# %%
response[0]["title"]
# %%
response[0]["link"]
# %%
html_doc = requests.get(response[0]["link"]).text
soup = BeautifulSoup(html_doc, "html.parser")
# %%
soup.get_text()
# %%
p_string = " ".join([x.get_text() for x in soup.find_all("p")])

# %%
cleaned_body = "".join(
    [
        p
        for p in p_string
        if p.isalnum()
        or p.isspace()
        or p in [".", ",", "!", "?", ":", ";", "'", '"', "(", ")"]
    ]
)
# %%
