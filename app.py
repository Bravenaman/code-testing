import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Black Friday AI Intelligence", layout="wide")

# ------------------ GOD UI ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #0f172a);
}
.main-header {
    font-size: 3.2rem;
    font-weight: 900;
    text-align: center;
    color: #00E5FF;
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,229,255,0.3);
}
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}
.metric {
    font-size: 2.2rem;
    color: #00E5FF;
    font-weight: bold;
}
.insight {
    background: rgba(0,229,255,0.1);
    border-left: 5px solid #00E5FF;
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight">⚡ {text}</div>', unsafe_allow_html=True)

# ------------------ DATA ------------------
@st.cache_data
def load():
    np.random.seed(42)
    n = 3000
    df = pd.DataFrame({
        "User_ID": np.random.randint(10000,15000,n),
        "Age": np.random.choice(['18-25','26-35','36-45','46-50'], n),
        "Gender": np.random.choice(['Male','Female'], n),
        "Occupation": np.random.randint(0,20,n),
        "Purchase": np.abs(np.random.normal(9000,3000,n)),
        "Category": np.random.choice(['Electronics','Apparel','Home','Beauty'], n)
    })

    df.loc[df['Age']=='26-35','Purchase'] += 3000
    df.loc[df['Age']=='36-45','Purchase'] += 4000

    df['Age_Code'] = df['Age'].map({'18-25':1,'26-35':2,'36-45':3,'46-50':4})

    scaler = StandardScaler()
    df['Scaled'] = scaler.fit_transform(df[['Purchase']])

    return df

df = load()

# ------------------ SIDEBAR ------------------
page = st.sidebar.radio("📊 Navigation", [
    "Stage 1: Scope",
    "Stage 2: Preprocessing",
    "Stage 3: EDA",
    "Stage 4: Clustering",
    "Stage 5: Association",
    "Stage 6: Anomaly",
    "Stage 7: Final"
])

# ------------------ HEADER ------------------
st.markdown('<div class="main-header">🛍️ AI Retail Intelligence System</div>', unsafe_allow_html=True)

# ------------------ STAGE 1 ------------------
if page == "Stage 1: Scope":
    st.markdown('<div class="glass">🎯 Goal: Understand customer behavior and maximize revenue using data.</div>', unsafe_allow_html=True)

# ------------------ STAGE 2 ------------------
elif page == "Stage 2: Preprocessing":
    st.markdown('<div class="glass">Data cleaned, encoded, and normalized for analysis.</div>', unsafe_allow_html=True)
    st.dataframe(df.head())

# ------------------ STAGE 3 ------------------
elif page == "Stage 3: EDA":
    fig = px.box(df, x="Age", y="Purchase", color="Gender",
                 color_discrete_map={'Male':'#00E5FF','Female':'#A259FF'},
                 template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    top_age = df.groupby('Age')['Purchase'].mean().idxmax()
    insight(f"Highest spending group is {top_age}.")

# ------------------ STAGE 4 ------------------
elif page == "Stage 4: Clustering":
    k = st.slider("Clusters",2,5,3)

    X = df[['Age_Code','Scaled']]
    model = KMeans(n_clusters=k,n_init=10)
    df['Cluster'] = model.fit_predict(X)

    cluster_avg = df.groupby('Cluster')['Purchase'].mean().sort_values()
    labels = ["Low","Mid","High","VIP","Elite"]
    mapping = {c:labels[i] for i,c in enumerate(cluster_avg.index)}
    df['Segment'] = df['Cluster'].map(mapping)

    fig = px.scatter(df, x="Age", y="Purchase", color="Segment",
                     template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    insight("High-value segments are your revenue drivers.")

# ------------------ STAGE 5 ------------------
elif page == "Stage 5: Association":
    transactions = df[['Category']].values.tolist()
    te = TransactionEncoder()
    df_te = pd.DataFrame(te.fit(transactions).transform(transactions), columns=te.columns_)

    freq = apriori(df_te, min_support=0.1, use_colnames=True)

    if not freq.empty:
        rules = association_rules(freq, metric="lift", min_threshold=1)
        st.dataframe(rules.head())

        insight("Product bundling opportunities detected.")

# ------------------ STAGE 6 ------------------
elif page == "Stage 6: Anomaly":
    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    upper = Q3 + 1.5*(Q3-Q1)

    df['Type'] = np.where(df['Purchase']>upper,"VIP","Normal")

    fig = px.histogram(df, x="Purchase", color="Type",
                       template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    insight("VIP customers identified for retention.")

# ------------------ STAGE 7 ------------------
elif page == "Stage 7: Final":
    insight("Target high-value clusters.")
    insight("Use bundling strategies.")
    insight("Retain VIP customers.")

# ------------------ FOOTER ------------------
st.markdown('<div class="glass">🚀 Built as an AI-powered decision system</div>', unsafe_allow_html=True)
