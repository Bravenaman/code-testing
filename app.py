import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Black Friday Insights", page_icon="🛍️", layout="wide")

# ------------------ LOAD & PREPROCESS (Stage 2) ------------------
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("BlackFriday.csv")
        
        # Encoding Gender: Male=0, Female=1 [cite: 43]
        df['Gender_Numeric'] = df['Gender'].map({'M': 0, 'F': 1})
        
        # Encoding Age groups into ordered numbers [cite: 44]
        age_mapping = {'0-17': 1, '18-25': 2, '26-35': 3, '36-45': 4, '46-50': 5, '51-55': 6, '55+': 7}
        df['Age_Encoded'] = df['Age'].map(age_mapping)
        
        # Handle missing values in Product Category 2 & 3 [cite: 42]
        df['Product_Category_2'] = df['Product_Category_2'].fillna(0)
        df['Product_Category_3'] = df['Product_Category_3'].fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_and_clean_data()

# ------------------ SIDEBAR NAVIGATION ------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "Project Scope", 
    "Exploratory Data Analysis", 
    "Customer Clustering", 
    "Product Intelligence", 
    "Anomaly Detection",
    "Final Recommendations"
])

# ------------------ STAGE 1: SCOPE [cite: 20] ------------------
if page == "Project Scope":
    st.header("Mining the Future: Black Friday Sales Insights")
    st.subheader("Project Objectives [cite: 27]")
    st.markdown("""
    * **Identify shopping behaviors** across demographics[cite: 28].
    * **Group customers** into distinct clusters[cite: 30].
    * **Find product combinations** often bought together[cite: 32].
    * **Detect unusual big spenders** (Anomalies)[cite: 33].
    """)
    st.write("### Dataset Preview", df.head())

# ------------------ STAGE 3: EDA [cite: 48] ------------------
elif page == "Exploratory Data Analysis":
    st.header("📊 Exploratory Data Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        # Purchase by Age & Gender [cite: 50]
        fig_age = px.box(df, x="Age", y="Purchase", color="Gender", title="Purchase Distribution by Age & Gender")
        st.plotly_chart(fig_age)
    
    with col2:
        # Popular Product Categories [cite: 51]
        cat_data = df['Product_Category_1'].value_counts().reset_index()
        fig_cat = px.bar(cat_data, x="Product_Category_1", y="count", title="Most Popular Product Categories")
        st.plotly_chart(fig_cat)

# ------------------ STAGE 4: CLUSTERING [cite: 56] ------------------
elif page == "Customer Clustering":
    st.header("🎯 Customer Segmentation (K-Means)")
    st.write("Grouping customers based on Age and Purchase habits[cite: 59].")
    
    # Feature Selection & Normalization [cite: 45, 59]
    cluster_data = df[['Age_Encoded', 'Purchase']].dropna()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(cluster_data)
    
    # Elbow Method [cite: 60]
    st.write("### Elbow Method")
    inertia = []
    for i in range(1, 8):
        km = KMeans(n_clusters=i, n_init=10, random_state=42).fit(scaled_features)
        inertia.append(km.inertia_)
    st.line_chart(inertia)
    
    k = st.slider("Select Number of Clusters", 2, 6, 3)
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    df['Cluster'] = model.fit_predict(scaled_features)
    
    # Visualization [cite: 62]
    fig_cluster = px.scatter(df.sample(5000), x="Age", y="Purchase", color="Cluster", title="Customer Segments")
    st.plotly_chart(fig_cluster)

# ------------------ STAGE 5: PRODUCT INTELLIGENCE [cite: 65, 69] ------------------
elif page == "Product Intelligence":
    st.header("🛒 Association Rule Mining (Apriori)")
    st.write("Discovering which product categories are bought together.")
    
    # Preparing data for Apriori
    # We create a 'basket' of Category 1, 2, and 3
    basket = df.sample(3000)[['User_ID', 'Product_Category_1', 'Product_Category_2', 'Product_Category_3']]
    basket = pd.get_dummies(basket.melt(id_vars='User_ID')['value'])
    basket = basket.groupby(level=0).max()
    
    # Apply Apriori 
    frequent_items = apriori(basket, min_support=0.05, use_colnames=True)
    if not frequent_items.empty:
        rules = association_rules(frequent_items, metric="lift", min_threshold=1)
        st.write("### Frequent Product Combinations")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    else:
        st.warning("Increase the sample size or lower support to see rules.")

# ------------------ STAGE 6: ANOMALY DETECTION  ------------------
elif page == "Anomaly Detection":
    st.header("🚨 Detecting Unusual Spenders")
    st.write("Identifying transactions that are significantly higher than average.")
    
    # IQR Method 
    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    
    df['Is_Anomaly'] = df['Purchase'] > upper_bound
    anomalies = df[df['Is_Anomaly'] == True]
    
    st.error(f"Detected {len(anomalies)} anomalies out of {len(df)} transactions.")
    fig_anom = px.histogram(df, x="Purchase", color="Is_Anomaly", title="Anomalies in Spending")
    st.plotly_chart(fig_anom)

# ------------------ STAGE 7: REPORTING  ------------------
elif page == "Final Recommendations":
    st.header("💡 Business Insights & Reporting")
    st.markdown(f"""
    * **Top Age Group:** The {df.groupby('Age')['Purchase'].sum().idxmax()} group contributes the most revenue.
    * **Gender Insights:** Analysis shows specific product categories dominate based on Gender.
    * **Cross-Selling:** High lift values in Association Rules suggest bundling Category {rules['antecedents'].iloc[0]} with Category {rules['consequents'].iloc[0]}.
    """)
