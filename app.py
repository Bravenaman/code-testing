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

    # Elbow Method
    inertia = []
    K = range(1, 8)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    fig_elbow = px.line(x=K, y=inertia, markers=True, title="Elbow Method")
    st.plotly_chart(fig_elbow, use_container_width=True)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    segment_map = {
        0: "Budget Buyers",
        1: "Regular Customers",
        2: "High Value Customers"
    }
    df['Segment'] = df['Cluster'].map(segment_map)

    fig = px.scatter(df, x="Age", y="Purchase", color="Segment",
                     title="Customer Segments")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ PRODUCT INTELLIGENCE ------------------
elif page == "🛒 Product Intelligence":
    st.title("Product Intelligence")
    st.write("Your rules and insights here")


# =========================================================
# 🛒 PRODUCT INTELLIGENCE
# =========================================================
elif page == "🛒 Product Intelligence":
    st.subheader("Market Basket Analysis")

    st.write("Discover which product categories are commonly purchased together.")

    try:
        # 🔥 Step 1: Sample data (prevents crash)
        sample_df = df.sample(n=5000, random_state=42)

        # 🔥 Step 2: Use ALL product categories
        basket_data = sample_df[['User_ID', 
                                 'Product_Category_1', 
                                 'Product_Category_2', 
                                 'Product_Category_3']]

        # Convert into long format
        basket_data = basket_data.melt(id_vars=['User_ID'], value_name='Product').dropna()

        # 🔥 Step 3: Create basket matrix
        basket = basket_data.groupby(['User_ID', 'Product'])['Product'] \
                            .count().unstack().fillna(0)

        # Convert to binary
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)

        # 🔥 Step 4: Apriori (lower threshold so rules actually appear)
        frequent = apriori(basket, min_support=0.01, use_colnames=True)

        # If no itemsets found → stop early
        if frequent.empty:
            st.warning("Not enough frequent itemsets found. Try increasing sample size.")
            st.stop()

        # 🔥 Step 5: Generate rules
        rules = association_rules(frequent, metric="lift", min_threshold=0.8)

        # 🔥 Step 6: Show results ONLY if they exist
        if not rules.empty:
            st.success(f"Found {len(rules)} association rules!")

            top_rules = rules.sort_values("lift", ascending=False).head(5)

            st.dataframe(top_rules[['antecedents', 'consequents',
                                    'support', 'confidence', 'lift']])

            st.markdown("### 🔍 Key Insights")

            for _, row in top_rules.iterrows():
                st.write(
                    f"If a user buys {list(row['antecedents'])}, "
                    f"they are likely to also buy {list(row['consequents'])} "
                    f"(Lift: {row['lift']:.2f}, Confidence: {row['confidence']:.2f})"
                )
        else:
            st.warning("No strong associations found. Try adjusting support levels.")

    except Exception as e:
        st.error(f"Error in Product Intelligence: {e}")
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
