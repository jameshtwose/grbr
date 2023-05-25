# %%
import os
import openai
from dotenv import load_dotenv, find_dotenv
# %%
_ = load_dotenv(find_dotenv())
# %%
openai.api_key = os.environ.get("OPENAI_API_KEY")
# %%
models = openai.Model.list()
[model.id for model in models.data][0:5]
# %%
test_prompt = "what are the latest innovations in sustainable plastics market?"
# %%
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user",
               "content": f"please reframe the following text to a prompt that will return a list of 5 links: {test_prompt}"}]
)
print(completion.choices[0].message.content)
# %%
links_prompt = completion.choices[0].message.content
# %%
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user",
               "content": links_prompt}]
)
print(completion.choices[0].message.content)
# %%
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr",
  temperature=0.7,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=1,
  stop=["\n"]
)
# %%
print(response.choices[0].text)
# %%
