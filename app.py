#customer segmentation
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from elbow import get_optimum_k

#page config
st.set_page_config(page_title = "Customer Segmentation",page_icon="assets/images.jpg",layout="wide")

with st.sidebar:
    st.title("Customer Segmentation")
    st.image("assets/images.jpg")

file = st.file_uploader("Upload datasets:",type=["csv","xlsx"])
if file:
    ext = file.name.split(".")[-1]
    if ext == "csv":
        df= pd.read_csv(file,index_col=[0])
    elif ext == "xlsx":
        df= pd.read_excel(file,index_col=[0])
    st.write(df)
    df.to_excel("customers.xlsx", index=False)

    columns = st.multiselect('Select Features:', options=df.columns)
    df = df[columns]

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)

    #find optimum number of clusters
    k = get_optimum_k(df)
    st.write(f"Optimum number of clusters: {k}")

    #kmeans clustering
    model = KMeans(n_clusters=k)
    model.fit(scaled)
    df["labels"] = model.labels_

    #scatter chart
    st.scatter_chart(x="Annual Income (k$)",y="Spending Score (1-100)",data=df,color="labels")

    # #DBSCAN
    # model = DBSCAN(eps=0.5, min_samples=5)
    # model.fit(df)
    # df["dbscan_labels"] = model.labels_
    # st.scatter_chart(x="Annual Income (k$)",y="Spending Score (1-100)",data=df,color="dbscan_labels")
