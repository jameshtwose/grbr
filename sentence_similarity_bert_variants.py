# %%
from sentence_transformers import SentenceTransformer, util

# %%
sentences = ["This is an example sentence", "Each sentence is converted"]
# %%
model_endpoint = 'kornwtp/ConGen-BERT-Tiny'
model = SentenceTransformer(model_endpoint.split('/')[1])
embeddings = model.encode(sentences)

# %%
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    # print("Embedding:", embedding)
    print(round(util.cos_sim(embeddings[0], embedding).item(), 4))
# %%
save_model = False
if save_model:
    model.save(model_endpoint.split('/')[1])
