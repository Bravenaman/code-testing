import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Black Friday Insights", page_icon="🛍️", layout="wide")

# ------------------ UI STYLING ------------------
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        .stMetric {
            background-color: #1c1f26;
            padding: 15px;
            border-radius: 10px;
        }
        h1, h2, h3 {
            color: #00ffd5;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ LOAD & PREPROCESS ------------------
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("BlackFriday.csv")
        
        df['Gender_Numeric'] = df['Gender'].map({'M': 0, 'F': 1})
        
        age_mapping = {'0-17': 1, '18-25': 2, '26-35': 3, '36-45': 4, '46-50': 5, '51-55': 6, '55+': 7}
        df['Age_Encoded'] = df['Age'].map(age_mapping)
        
        df['Product_Category_2'] = df['Product_Category_2'].fillna(0)
        df['Product_Category_3'] = df['Product_Category_3'].fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_and_clean_data()

# ------------------ KPI DASHBOARD ------------------
st.title("🛍️ Black Friday Intelligence Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${df['Purchase'].sum():,.0f}")
col2.metric("Avg Purchase", f"${df['Purchase'].mean():.2f}")
col3.metric("Total Customers", df['User_ID'].nunique())
col4.metric("Top Category", df['Product_Category_1'].mode()[0])

# ------------------ SIDEBAR ------------------
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio("Go to:", [
    "Project Scope", 
    "Exploratory Data Analysis", 
    "Customer Clustering", 
    "Product Intelligence", 
    "Anomaly Detection",
    "Final Recommendations"
])

# ------------------ PROJECT SCOPE ------------------
if page == "Project Scope":
    st.header("Mining the Future: Black Friday Sales Insights")
    st.markdown("""
    * Identify shopping behaviors across demographics
    * Group customers into clusters
    * Find product combinations
    * Detect unusual big spenders
    """)
    st.write("### Dataset Preview", df.head())

# ------------------ EDA ------------------
elif page == "Exploratory Data Analysis":
    st.header("📊 Exploratory Data Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_age = px.box(df, x="Age", y="Purchase", color="Gender", title="Purchase Distribution by Age & Gender")
        st.plotly_chart(fig_age)
    
    with col2:
        cat_data = df['Product_Category_1'].value_counts().reset_index()
        fig_cat = px.bar(cat_data, x="Product_Category_1", y="count", title="Most Popular Product Categories")
        st.plotly_chart(fig_cat)

    st.subheader("📌 Key Insights")

    top_age = df.groupby('Age')['Purchase'].mean().idxmax()
    top_gender = df.groupby('Gender')['Purchase'].mean().idxmax()

    st.success(f"""
    - Customers aged **{top_age}** spend the most on average.
    - **{top_gender} customers** tend to have higher purchase values.
    - Category **{df['Product_Category_1'].mode()[0]}** is the most popular.
    """)

# ------------------ CLUSTERING ------------------
elif page == "Customer Clustering":
    st.header("🎯 Customer Segmentation (K-Means)")
    
    cluster_data = df[['Age_Encoded', 'Purchase']].dropna()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(cluster_data)
    
    inertia = []
    for i in range(1, 8):
        km = KMeans(n_clusters=i, n_init=10, random_state=42).fit(scaled_features)
        inertia.append(km.inertia_)
    st.line_chart(inertia)
    
    k = st.slider("Select Number of Clusters", 2, 6, 3)
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    df['Cluster'] = model.fit_predict(scaled_features)
    
    fig_cluster = px.scatter(df.sample(5000), x="Age", y="Purchase", color="Cluster", title="Customer Segments")
    st.plotly_chart(fig_cluster)

    cluster_summary = df.groupby('Cluster')['Purchase'].mean().sort_values()

    st.subheader("🧠 Cluster Insights")

    for i, val in cluster_summary.items():
        st.write(f"Cluster {i}: Avg Purchase = ${val:.2f}")

    high_value_cluster = cluster_summary.idxmax()

    st.success(f"""
    - Cluster {high_value_cluster} represents **high-value customers**.
    - These users should be targeted with **premium offers and early access deals**.
    """)

# ------------------ PRODUCT INTELLIGENCE ------------------
elif page == "Product Intelligence":
    st.header("🛒 Association Rule Mining (Apriori)")
    
    basket = df.sample(3000)[['User_ID', 'Product_Category_1', 'Product_Category_2', 'Product_Category_3']]
    basket = pd.get_dummies(basket.melt(id_vars='User_ID')['value'])
    basket = basket.groupby(level=0).max()
    
    frequent_items = apriori(basket, min_support=0.05, use_colnames=True)

    if not frequent_items.empty:
        rules = association_rules(frequent_items, metric="lift", min_threshold=1)

        st.subheader("📊 Strongest Product Bundles")

        rules = rules.sort_values(by="lift", ascending=False)
        top_rules = rules.head(5)

        for i, row in top_rules.iterrows():
            st.write(f"""
            🔹 If a user buys **{list(row['antecedents'])}**,  
            they are likely to also buy **{list(row['consequents'])}**  
            (Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})
            """)
    else:
        st.warning("Increase the sample size or lower support to see rules.")

# ------------------ ANOMALY DETECTION ------------------
elif page == "Anomaly Detection":
    st.header("🚨 Detecting Unusual Spenders")
    
    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    
    df['Is_Anomaly'] = df['Purchase'] > upper_bound
    anomalies = df[df['Is_Anomaly'] == True]
    
    st.error(f"Detected {len(anomalies)} anomalies out of {len(df)} transactions.")

    fig_anom = px.histogram(df, x="Purchase", color="Is_Anomaly", title="Anomalies in Spending")
    st.plotly_chart(fig_anom)

    st.subheader("🚨 Insight")

    if len(anomalies) > 0:
        st.warning(f"""
        - Top {len(anomalies)} transactions are unusually high.
        - These may represent **VIP customers or bulk buyers**.
        - Businesses should target them with loyalty rewards.
        """)

# ------------------ FINAL RECOMMENDATIONS ------------------
elif page == "Final Recommendations":
    st.header("💡 Final Business Strategy")

    top_age = df.groupby('Age')['Purchase'].sum().idxmax()
    top_cluster = df.groupby('Cluster')['Purchase'].mean().idxmax()

    st.success(f"""
    ### 🎯 Target Audience
    - Age Group: **{top_age}**
    - Customer Segment: **Cluster {top_cluster} (High Spenders)**

    ### 🛒 Sales Strategy
    - Bundle frequently bought products together
    - Offer discounts on high-lift combinations

    ### 💰 Revenue Boost Strategy
    - Focus marketing on high-value clusters
    - Retarget anomaly customers (big spenders)

    ### 🚀 Final Takeaway
    This data shows that **not all customers are equal** — focusing on high-value segments will maximize profit.
    """)
