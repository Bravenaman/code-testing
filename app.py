import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="RetailMind AI", page_icon="🛍️", layout="wide")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    try:
        # Using a sample or full dataset as per Stage 2 [cite: 254]
        df = pd.read_csv("BlackFriday.csv")
        # Preprocessing [cite: 256, 257, 258]
        df['Gender_Code'] = df['Gender'].map({'Male': 0, 'Female': 1})
        # Mapping Age groups to ordered numbers 
        age_map = {'0-17':1, '18-25':2, '26-35':3, '36-45':4, '46-50':5, '51-55':6, '55+':7}
        df['Age_Code'] = df['Age'].map(age_map)
        # Handle missing values [cite: 256]
        df['Product_Category_2'] = df['Product_Category_2'].fillna(0)
        df['Product_Category_3'] = df['Product_Category_3'].fillna(0)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# ------------------ SIDEBAR NAVIGATION ------------------
with st.sidebar:
    st.title("WACP Data Mining")
    page = st.radio("Stages", [
        "1. Project Scope",
        "2. EDA & Visuals",
        "3. Customer Clustering",
        "4. Product Intelligence",
        "5. Anomaly Detection",
        "6. Final Insights"
    ])

# ------------------ STAGE 1: PROJECT SCOPE [cite: 234] ------------------
if page == "1. Project Scope":
    st.header("🎯 Stage 1: Define Project Scope")
    st.markdown("""
    **Objective:** Analyze Black Friday retail sales to uncover customer segments and product associations[cite: 237].
    * **Target:** InsightMart Analytics Retail Chain[cite: 218].
    * **Key Metrics:** Purchase patterns, demographics, and high-spender detection[cite: 242, 247].
    """)
    st.dataframe(df.head(10))

# ------------------ STAGE 2: EDA [cite: 262] ------------------
elif page == "2. EDA & Visuals":
    st.header("📊 Stage 2: Exploratory Data Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Purchase by Gender [cite: 264]
        fig1 = px.box(df, x="Gender", y="Purchase", title="Purchase Distribution by Gender")
        st.plotly_chart(fig1)
        
    with col2:
        # Popular Categories [cite: 265]
        cat_counts = df['Product_Category_1'].value_counts().reset_index()
        fig2 = px.bar(cat_counts, x="Product_Category_1", y="count", title="Top Product Categories")
        st.plotly_chart(fig2)

# ------------------ STAGE 3: CLUSTERING [cite: 270] ------------------
elif page == "3. Customer Clustering":
    st.header("🎯 Stage 3: Customer Segmentation")
    # Prepare features for K-Means [cite: 273]
    X = df[['Age_Code', 'Purchase']].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Elbow Method [cite: 274]
    st.subheader("Elbow Method to Find Optimal K")
    inertia = [KMeans(n_clusters=k, n_init=10).fit(X_scaled).inertia_ for k in range(1, 7)]
    st.line_chart(inertia)
    
    k = st.slider("Select Clusters", 2, 5, 3)
    model = KMeans(n_clusters=k, n_init=10)
    df['Cluster'] = model.fit_predict(X_scaled)
    
    fig = px.scatter(df.sample(5000), x="Age", y="Purchase", color="Cluster", title="Customer Segments")
    st.plotly_chart(fig)

# ------------------ STAGE 4: PRODUCT INTELLIGENCE (FIXED) [cite: 279] ------------------
elif page == "4. Product Intelligence":
    st.header("🛒 Stage 4: Association Rule Mining")
    st.info("Finding product combinations often bought together[cite: 246].")
    
    # Simulating Market Basket by grouping categories per User 
    basket_df = df.sample(2000).groupby(['User_ID', 'Product_Category_1'])['Product_Category_1'].count().unstack().fillna(0)
    basket_sets = basket_df.applymap(lambda x: 1 if x > 0 else 0)
    
    # Apriori Algorithm 
    frequent_itemsets = apriori(basket_sets, min_support=0.05, use_colnames=True)
    if not frequent_itemsets.empty:
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        st.write("### Frequent Product Rules")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    else:
        st.warning("No frequent associations found with current support threshold.")

# ------------------ STAGE 5: ANOMALY DETECTION  ------------------
elif page == "5. Anomaly Detection":
    st.header("🚨 Stage 5: Detecting Unusual Spenders")
    # Using Z-Score as suggested in Stage 6 
    threshold = df['Purchase'].mean() + (3 * df['Purchase'].std())
    anomalies = df[df['Purchase'] > threshold]
    
    st.write(f"Detected **{len(anomalies)}** unusually high transactions (Threshold: ${threshold:,.2f})")
    fig = px.histogram(df, x="Purchase", color=df['Purchase'] > threshold, title="Spending Anomalies")
    st.plotly_chart(fig)

# ------------------ STAGE 6: REPORTING [cite: 365] ------------------
elif page == "6. Final Insights":
    st.header("📋 Stage 6: Strategic Recommendations")
    st.markdown(f"""
    1. **Primary Spenders:** The **{df.groupby('Age')['Purchase'].sum().idxmax()}** age group shows the highest total spending.
    2. **Gender Preference:** { "Males" if df[df['Gender']=='M']['Purchase'].mean() > df[df['Gender']=='F']['Purchase'].mean() else "Females" } spend more on average.
    3. **Strategy:** Target 'Premium Buyers' (Cluster 1) with loyalty rewards for High-Category items.
    """)
