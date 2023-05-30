# %%
import requests
from bs4 import BeautifulSoup
# %%
html_doc = requests.get("https://www.google.com/alerts/feeds/17740685286653827239/3974289959828158708").text
# %%
soup = BeautifulSoup(html_doc, features="xml")
# %%
soup.get_text()
# %%
for entry in soup.find_all("entry"):
    print(entry.title.get_text())
    print(entry.link["href"])
    print(entry.published.get_text())
    print(entry.content.get_text())

# %%
new_link_doc = requests.get(entry.link["href"]).text
# %%
new_soup = BeautifulSoup(new_link_doc, "html.parser")
# %%
new_soup.get_text()
# %%
for entry in soup.find_all("entry"):
    print(entry.link["href"].split("url=")[1].split("&ct=")[0])
# %%
response = requests.get(
    entry.link["href"].split("url=")[1].split("&ct=")[0],
)
# %%
link_soup = BeautifulSoup(response.text, "html.parser")
# %%
find_list = [x.get_text() for x in link_soup.find_all(["h1", "h2", "h3", "h4", "h5", "p"])]
# %%
" ".join(find_list)
# %%
