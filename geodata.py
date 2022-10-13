import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

g_cols = ["Country Name", "Indicator Name", "2018"]
raw_data = pd.read_csv('WDIData.csv')[g_cols]  ### World Bank data.

g_cols = ["Country Name", "Indicator Name", "2018"]
social_columns = [ 'Government expenditure on education, total (% of GDP)',
                      'Current health expenditure (% of GDP)',
                     'Government expenditure on education, total (% of government expenditure)',
                      'Domestic general government health expenditure (% of general government expenditure)',
                     'Gini index'
                    ]
gap_columns = [x for x in raw_data["Indicator Name"].unique() if "gap" in x]
exp_columns = [x for x in raw_data["Indicator Name"].unique() if "expenditure" in x.lower()]
gdp_columns = list(set([x for x in df.columns if "(% of GDP)" in x]))

df = raw_data.groupby(by=["Indicator Name", "Country Name"], as_index=False).mean()
df = df.pivot(columns=["Indicator Name"], index="Country Name")
df.columns = [x[1] for x in df.columns]

def clustering(df, columns, t=0.5): 
    df = df.dropna(axis=1, thresh=int(t*len(df)))
    columns = [x for x in columns if x in df.columns]
    df = df[columns]
    df = df.dropna()
    cols = df.columns
    for i in range(5, 21, 5):
        reg = KMeans(n_clusters=i).fit(df[cols].to_numpy())
        df.loc[:, f"clusters_{i}"] = reg.labels_
    return df 

df = clustering(df, exp_columns)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df = df.reset_index().rename(columns={"Country Name": 'name'})
d = {
    "Russia": "Russian Federation", 
    'United States of America': 'United States',   
    'Korea, Rep.': "South Korea",
    'Slovakia': "Slovak Republic", 
    'Czechia': "Czech Republic",
    "Egypt": 'Egypt, Arab Rep.',
    'Iran':  'Iran, Islamic Rep.',
    'Turkey': "Turkiye",
    "Kyrgyzstan":  'Kyrgyz Republic',
    "Yemen": "Yemen, Rep.",
    'Bosnia and Herz.': 'Bosnia and Herzegovina'
}
world['name'] = [d.get(i, i) for i in world['name']]
gdf = gpd.GeoDataFrame(pd.merge(world[['name', 'geometry']], df, how='left', on='name').dropna())

gdf.plot("clusters_5", figsize=(15, 15), cmap="plasma", edgecolor='black').set(title="Clusters by expenditures")
print(gdf.columns.shape)
