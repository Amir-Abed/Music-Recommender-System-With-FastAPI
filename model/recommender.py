# for detailed explanation refer to showcase.ipynb

from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("./static/dataset/Data/features_30_sec.csv", index_col="filename")
df_api = pd.read_csv("./static/dataset/Data/features_30_sec.csv")

# preparing a dictionaray with "label" as key and "filename" as value
# then we'll be able to fetch it via app.js
labels_df = df_api["label"]
labels_df.index = df_api["filename"]
data_to_send = labels_df.to_dict()

labels = df["label"]
features = df.drop(["length", "label"], axis=1)

features_scaled = preprocessing.scale(features)

similarity = cosine_similarity(features_scaled)
similarity_df = pd.DataFrame(similarity)

similarity_df_names = similarity_df.set_index(labels.index)
similarity_df_names.columns = labels.index

similarity_df_names.head()

dest_path = "./static/dataset/Data/genres_original"
def find_similar_songs(name, rec_n):
    similarities = similarity_df_names[name].sort_values(ascending=False)
    similarities = similarities.drop(name)
    print(f"similar songs to {name}:\n")
    return similarities.head(rec_n)