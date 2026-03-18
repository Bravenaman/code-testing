import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="RetailMind AI", page_icon="🧠", layout="wide")

# ------------------ CUSTOM STYLE ------------------
st.markdown("""
<style>
.stApp { background-color: #0B0F19; color: #E5E7EB; }
section[data-testid="stSidebar"] { background-color: #111827; }
h1, h2, h3 { color: #F9FAFB; }
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("BlackFriday.csv")
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please upload the file.")
        return None

df = load_data()

if df is None:
    st.stop()

# ------------------ PREPROCESSING ------------------
df['Age_Code'] = df['Age'].astype('category').cat.codes
df['Gender_Code'] = df['Gender'].map({'Male': 0, 'Female': 1})

df.fillna(0, inplace=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.title("RetailMind AI")
    page = st.radio("Navigation", [
        "📌 Project Overview",
        "📊 Dashboard",
        "📈 Customer Insights",
        "🎯 Segmentation",
        "🛒 Product Intelligence",
        "🚨 Anomalies"
    ])

# ------------------ HEADER ------------------
st.title("🧠 RetailMind AI")
st.caption("Data-Driven Black Friday Intelligence System")

# ------------------ KPIs ------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${df['Purchase'].sum():,.0f}")
col2.metric("Avg Purchase", f"${df['Purchase'].mean():,.2f}")
col3.metric("Customers", df['User_ID'].nunique())
col4.metric("High Spenders", len(df[df['Purchase'] > 20000]))

st.divider()

# =========================================================
# 📊 DASHBOARD
# =========================================================
if page == "📌 Project Overview":
    st.title("🛍️ Black Friday Sales Analysis")

    # ------------------ OBJECTIVES ------------------
    st.markdown("## 🎯 Project Objectives")

    st.markdown("""
    **Primary Goal:**  
    Analyze customer purchasing behavior during Black Friday sales to uncover patterns and improve business decision-making.

    **Secondary Goals:**
    - Segment customers using clustering (K-Means)
    - Identify product associations using Apriori algorithm
    - Understand spending patterns across demographics
    - Generate actionable insights for marketing strategies
    """)

    st.markdown("---")

    # ------------------ PROJECT SCOPE ------------------
    st.markdown("## 🌍 Project Scope")

    st.markdown(f"""
    - **Dataset:** Black Friday Sales Dataset  
    - **Records:** {df.shape[0]} transactions  
    - **Features:** {df.shape[1]} attributes  
    - **Key Variables:** Age, Gender, Occupation, Product Categories, Purchase Amount  
    - **Analysis Focus:** Customer behavior, product trends, and spending habits  
    """)

    st.markdown("---")

    # ------------------ TASKS PERFORMED ------------------
    st.markdown("## 🧠 Tasks Performed")

    st.markdown("""
    1. **Data Cleaning & Preprocessing**
       - Handled missing values in product categories  
       - Encoded categorical variables (Gender, Age)  

    2. **Exploratory Data Analysis (EDA)**
       - Distribution of purchase amounts  
       - Demographic-based analysis  

    3. **Customer Segmentation**
       - Applied K-Means clustering  
       - Identified distinct customer groups  

    4. **Product Intelligence**
       - Used Apriori algorithm  
       - Generated association rules between product categories  

    5. **Visualization**
       - Built interactive charts using Plotly  
    """)

    st.markdown("---")
    st.markdown("# 📊 Dataset Overview")

    col1, col2 = st.columns([2, 1])

    # ------------------ FEATURES DESCRIPTION ------------------
    with col1:
        st.markdown("## 🧾 Features Description")

        feature_df = pd.DataFrame({
            "Feature": df.columns,
            "Type": df.dtypes.astype(str),
            "Sample Value": [
                str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "N/A"
                for col in df.columns
            ]
        })

        st.dataframe(feature_df)

    # ------------------ DATA QUALITY ------------------
    with col2:
        st.markdown("## ✅ Data Quality")

        missing_values = df.isnull().sum().sum()

        if missing_values == 0:
            st.success("✨ No missing values in dataset")
        else:
            st.warning(f"⚠️ Dataset has {missing_values} missing values")

        st.markdown("### 📌 Quick Stats")
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.write(f"Unique Users: {df['User_ID'].nunique()}")
        
        st.markdown("---")

    # ------------------ SAMPLE DATA ------------------
    st.markdown("## 🔍 Sample Data")
    st.dataframe(df.head(10))
        

# =========================================================
# 📊 DASHBOARD
# =========================================================
elif page == "📊 Dashboard":
    st.subheader("Business Overview")

    fig = px.histogram(df, x="Purchase", nbins=50, title="Purchase Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:** Most purchases are concentrated in the mid-range, while a small group of users contribute to extremely high transactions.
    """)

# =========================================================
# 📈 CUSTOMER INSIGHTS
# =========================================================
elif page == "📈 Customer Insights":
    st.subheader("Customer Behavior Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(df, x="Age", y="Purchase", color="Gender",
                     title="Purchase by Age & Gender")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(df.groupby("Product_Category_1")["Purchase"].mean().reset_index(),
                     x="Product_Category_1", y="Purchase",
                     title="Avg Spend per Product Category")
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 🎯 SEGMENTATION
# =========================================================

elif page == "🎯 Segmentation":
    st.subheader("Customer Segmentation (K-Means)")

    features = ['Age_Code', 'Purchase']
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    # ------------------ ELBOW METHOD ------------------
    st.markdown("### 📉 Elbow Method (Find Optimal K)")

    inertia = []
    K = range(1, 8)
    for k_val in K:
        kmeans = KMeans(n_clusters=k_val, random_state=42, n_init=10)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    fig_elbow = px.line(x=K, y=inertia, markers=True, title="Elbow Method")
    st.plotly_chart(fig_elbow, use_container_width=True)

    # ------------------ INTERACTIVE K ------------------
    st.markdown("### ⚙️ Choose Number of Segments")

    k = st.slider("Select number of clusters (k):", 2, 7, 3)

    # ------------------ APPLY KMEANS ------------------
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X)

    # ------------------ DYNAMIC LABELING ------------------
    cluster_means = df.groupby('Cluster')['Purchase'].mean().sort_values()

    labels = {}
    for i, cluster in enumerate(cluster_means.index):
        if i == 0:
            labels[cluster] = "Budget Buyers"
        elif i == len(cluster_means) - 1:
            labels[cluster] = "High Value Customers"
        else:
            labels[cluster] = "Regular Customers"

    df['Segment'] = df['Cluster'].map(labels)

    # ------------------ VISUALIZATION ------------------
    st.markdown("### 📊 Customer Segments Visualization")

    fig = px.scatter(
        df,
        x="Age",
        y="Purchase",
        color="Segment",
        title=f"Customer Segments (k={k})",
        opacity=0.7
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------ SUMMARY TABLE ------------------
    st.markdown("### 📋 Segment Summary")

    summary = df.groupby('Segment')['Purchase'].mean().reset_index()
    st.dataframe(summary)

# ------------------ PRODUCT INTELLIGENCE ------------------
elif page == "🛒 Product Intelligence":
    st.title("Product Intelligence")
    st.write("Your rules and insights here")


# =========================================================
# 🛒 PRODUCT INTELLIGENCE
# =========================================================
elif page == "🛒 Product Intelligence":
    st.title("🛒 Product Intelligence")

    # =========================================================
    # 🧠 INTRO
    # =========================================================
    st.markdown("### 🧠 What is this?")
    st.write(
        "This section analyzes customer purchase behavior to identify "
        "which product categories are frequently bought together."
    )

    try:
        # =========================================================
        # 📊 DATA PREPARATION
        # =========================================================
        st.markdown("### 📊 Market Basket Analysis")

        sample_df = df.sample(n=5000, random_state=42)

        basket_data = sample_df[['User_ID',
                                 'Product_Category_1',
                                 'Product_Category_2',
                                 'Product_Category_3']]

        # Convert to long format
        basket_data = basket_data.melt(id_vars=['User_ID'], value_name='Product')
        basket_data = basket_data.dropna()

        # Convert to string (important)
        basket_data['Product'] = basket_data['Product'].astype(str)

        # Create basket matrix
        basket = basket_data.groupby(['User_ID', 'Product'])['Product'] \
                            .count().unstack().fillna(0)

        basket = basket.applymap(lambda x: 1 if x > 0 else 0)

        st.write("📦 Basket size:", basket.shape)

        # =========================================================
        # ⚙️ USER CONTROL
        # =========================================================
        st.markdown("### ⚙️ Adjust Analysis Sensitivity")

        min_support = st.slider("Minimum Support", 0.001, 0.05, 0.01)

        # =========================================================
        # 🧮 APRIORI MODEL
        # =========================================================
        from mlxtend.frequent_patterns import apriori, association_rules

        frequent = apriori(basket, min_support=min_support, use_colnames=True)

        if frequent.empty:
            st.warning("No frequent itemsets found. Try lowering support.")
            st.stop()

        rules = association_rules(frequent, metric="confidence", min_threshold=0.1)

        st.success(f"✅ Found {len(rules)} association rules")

        # =========================================================
        # 📋 RULES TABLE
        # =========================================================
        st.markdown("### 📋 Top Association Rules")

        top_rules = rules.sort_values("lift", ascending=False).head(5)

        st.dataframe(top_rules[['antecedents', 'consequents',
                                'support', 'confidence', 'lift']])

        # =========================================================
        # 🔍 INSIGHTS
        # =========================================================
        st.markdown("### 🔍 Key Insights")

        for _, row in top_rules.iterrows():
            st.write(
                f"Customers who buy {list(row['antecedents'])} "
                f"are likely to also buy {list(row['consequents'])} "
                f"(Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})"
            )

        # =========================================================
        # 💡 BUSINESS RECOMMENDATIONS
        # =========================================================
        st.markdown("### 💡 Business Recommendations")

        st.write("• Bundle frequently bought products together")
        st.write("• Place associated items near each other in-store")
        st.write("• Offer combo discounts to increase average order value")
        st.write("• Use targeted ads based on purchase behavior")

        # =========================================================
        # 📊 BONUS VISUAL
        # =========================================================
        st.markdown("### 📊 Most Frequent Products")

        top_products = basket.sum().sort_values(ascending=False).head(10)

        import plotly.express as px
        fig = px.bar(
            x=top_products.index,
            y=top_products.values,
            labels={'x': 'Product Category', 'y': 'Frequency'},
            title="Top Purchased Product Categories"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error in Product Intelligence: {e}")
# =========================================================
# 🚨 ANOMALIES
# =========================================================
elif page == "🚨 Anomalies":
    st.subheader("Anomaly Detection")

    # Z-score method
    mean = df['Purchase'].mean()
    std = df['Purchase'].std()

    threshold = mean + 3 * std
    df['Anomaly'] = df['Purchase'] > threshold

    fig = px.scatter(df, x=df.index, y="Purchase", color="Anomaly",
                     title="Outlier Detection")
    fig.add_hline(y=threshold, line_dash="dash")

    st.plotly_chart(fig, use_container_width=True)

    st.error(f"{df['Anomaly'].sum()} anomalies detected")

    st.markdown("""
    **Insight:** These users spend significantly more than average and may represent VIP customers or unusual transactions.
    """)
