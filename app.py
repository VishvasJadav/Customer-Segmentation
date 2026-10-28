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

    columns = st.multiselect(
        "Select Features:",
        options=df.columns.tolist(),
        default=[]
    )

    # Check whether features have been selected
    if not columns:
        st.warning("Please select at least one feature to continue.")
        st.stop()

    # Select features
    df = df[columns].copy()

    # Ensure selected features are numeric
    non_numeric = df.select_dtypes(exclude=["number"]).columns.tolist()

    if non_numeric:
        st.error(f"Please select numeric features only. Non-numeric columns: {non_numeric}")
        st.stop()

    # Handle missing values
    df = df.dropna()

    if df.empty:
        st.error("No valid rows remain after removing missing values.")
        st.stop()

    if df.shape[1] == 0:
        st.error("Please select at least one numeric feature.")
        st.stop()

    # Scale features
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)

    # Find optimum number of clusters
    k = get_optimum_k(df)
    st.write(f"Optimum number of clusters: {k}")

    if k < 2 or k > len(df):
        st.error("The number of clusters must be between 2 and the number of valid rows.")
        st.stop()

    # KMeans clustering
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(scaled)
    df["labels"] = model.labels_

    # Scatter chart
    if (
        "Annual Income (k$)" in df.columns
        and "Spending Score (1-100)" in df.columns
    ):
        st.scatter_chart(
            x="Annual Income (k$)",
            y="Spending Score (1-100)",
            data=df,
            color="labels"
        )
    else:
        st.info(
            "To display the customer segmentation scatter chart, "
            "select Annual Income (k$) and Spending Score (1-100)."
        )

    st.subheader("Clustered Customer Data")
    st.write(df)
    # #DBSCAN
    # model = DBSCAN(eps=0.5, min_samples=5)
    # model.fit(df)
    # df["dbscan_labels"] = model.labels_
    # st.scatter_chart(x="Annual Income (k$)",y="Spending Score (1-100)",data=df,color="dbscan_labels")
