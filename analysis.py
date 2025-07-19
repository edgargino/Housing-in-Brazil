# Import Matplotlib, pandas, and plotly
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Note that the CSV files are missing currently but this code would give a
# Few graphs with perspective into the brazilian housing market with the right data.

df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df1.head()

df1 = df1.dropna()

df1[["lat", "lon"]] = df1["lat-lon"].str.split(',',expand=True)
df1 = df1.drop("lat-lon", axis=1)
df1["lat"] = df1["lat"].astype(float)
df1["lon"] = df1["lon"].astype(float)

df1["state"] = df1["place_with_parent_names"].str.split('|', expand=True)[2]
df1 = df1.drop("place_with_parent_names", axis=1)

df1["price_usd"] = df1["price_usd"].str.replace("$","", regex=False)
df1["price_usd"] = df1["price_usd"].str.replace(",","", regex=False)
df1["price_usd"] = df1["price_usd"].astype(float)

df2 = pd.read_csv("data/brasil-real-estate-2.csv")
df2.head()

df2["price_usd"] = (df2["price_brl"] / 3.19).round(2)
df2

df3 = pd.DataFrame()
df2 = df2.dropna()
df2.head()

df3["property_type"] = df2["property_type"]
df3["region"] = df2["region"]
df3["area_m2"] = df2["area_m2"]
df3["price_usd"] = df2["price_usd"]
df3["lat"] = df2["lat"]
df3["lon"] = df2["lon"]

df = pd.concat([df1,df2])
print("df shape:", df.shape)

fig = px.scatter_mapbox(
    df,
    lat="lat", 
    lon="lon", 
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()


summary_stats = df[["area_m2","price_usd"]].describe()
summary_stats

fig, ax = plt.subplots()

# Build histogram
ax.hist(df["price_usd"][0:20001], bins = 10)

# Label axes
plt.xlabel("Price [USD]")
plt.ylabel("Frequency")

# Add title
plt.title("Distribution of Home Prices")

fig, ax = plt.subplots()

#Build box plot
ax.boxplot(df["area_m2"], vert=False)

# Label x-axis
plt.xlabel("Area [sq meters]")
# Add title
plt.title("Distribution of Home Sizes")

mean_price_by_region = df.groupby("region")["price_usd"].mean()
mean_price_by_region

fig, ax = plt.subplots()

df_south = df.loc[df['region']=="South"]
df_south.head()

# Build bar chart, label axes, add title
mean_price_by_region.plot(kind="bar",title="Mean Home Price by Region", xlabel="Region", ylabel="Mean Price [USD]", ax=ax)

homes_by_state = df_south['state'].value_counts()

# Subset data
df_south_rgs = df_south.loc[df_south['state']=="Rio Grande do Sul"]

# Don't change the code below 👇
fig, ax = plt.subplots()

# Build scatter plot
ax.scatter(df_south_rgs['area_m2'], df_south_rgs['price_usd'])

# Label axes
ax.set_xlabel('Area [sq meters]')
ax.set_ylabel('Price [USD]')

# Add title
ax.set_title('Rio Grande do Sul: Price vs. Area')

print(areas)
south_states_corr = dict()
for i in df_south['state'].unique():
    a = df_south[df_south['state'] == i]
    south_states_corr[i] = a['area_m2'].corr(a['price_usd'])

south_states_corr