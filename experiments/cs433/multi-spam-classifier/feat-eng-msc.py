import pandas as pd
from bs4 import BeautifulSoup

KEEP = ['description', 'spam']
SPAMS = pd.DataFrame()
HAMS = pd.DataFrame()

for chunk in pd.read_json('zenodo_open_metadata_2020-10-19.jsonl', lines=True, chunksize=100000):
    chunk = chunk[KEEP].dropna()
    
    chunk_spams = chunk[chunk['spam'] == True]
    chunk_spams['description'] = chunk_spams['description'].map(lambda x: BeautifulSoup(x, 'html.parser').get_text())
    chunk_spams['spam'] = chunk_spams['spam'].map(lambda x: 1)
    SPAMS = pd.concat([SPAMS, chunk_spams])

    chunk_hams = chunk[chunk['spam'] == False]
    chunk_hams['description'] = chunk_hams['description'].map(lambda x: BeautifulSoup(x, 'html.parser').get_text())
    chunk_hams['spam'] = chunk_hams['spam'].map(lambda x: 0)
    HAMS = pd.concat([HAMS, chunk_hams])
    
HAMS = HAMS.sample(n= 2*len(SPAMS))
df = pd.concat([SPAMS, HAMS]).rename(columns={'spam': 'label'})

df.to_csv('dataset-msc.csv', index=False)