import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import warnings
warnings.filterwarnings('ignore')

# ------------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="Black Friday Intelligence",
    page_icon="🛍️",
    layout="wide"
)

# ------------------------------
# 🔥 REMASTERED UI (YOUR IDENTITY)
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: 900;
    color: #00E5FF;
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, #0a0a0a, #1a1a2e);
    border-radius: 12px;
    border-bottom: 3px solid #A259FF;
}
.sub-header {
    text-align: center;
    color: #ccc;
    margin-bottom: 2rem;
}
.card {
    background: linear-gradient(145deg, #111827, #1f2937);
    padding: 25px;
    border-radius: 15px;
    border-left: 5px solid #A259FF;
    margin-bottom: 20px;
}
.metric-card {
    background: #020617;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #00E5FF;
    text-align: center;
}
.metric-value {
    font-size: 2.3rem;
    color: #00E5FF;
}
.metric-label {
    color: #ccc;
}
.info-box {
    background: #0f172a;
    border-left: 5px solid #00E5FF;
    padding: 15px;
    margin: 10px 0;
}
.footer {
    text-align: center;
    color: #888;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

def show_insight(text):
    st.markdown(f'<div class="info-box">⚡ <b>Key Insight:</b> {text}</div>', unsafe_allow_html=True)

# ------------------------------
# DATA GENERATION (SMART)
@st.cache_data
def load_data():
    np.random.seed(42)
    size = 2500

    df = pd.DataFrame({
        'User_ID': np.random.randint(10000, 15000, size),
        'Gender': np.random.choice(['Male', 'Female'], size),
        'Age': np.random.choice(['18-25','26-35','36-45','46-50'], size),
        'Occupation': np.random.randint(0, 20, size),
        'Product_Category_1': np.random.choice(['Electronics','Apparel','Home','Beauty'], size),
        'Product_Category_2': np.random.choice(['Accessories','Footwear','Decor',None], size),
        'Purchase': np.abs(np.random.normal(9000,3000,size))
    })

    df['Product_Category_2'].fillna("None", inplace=True)

    df['Gender_Code'] = df['Gender'].map({'Male':0,'Female':1})
    df['Age_Code'] = df['Age'].map({'18-25':1,'26-35':2,'36-45':3,'46-50':4})

    scaler = StandardScaler()
    df['Purchase_Scaled'] = scaler.fit_transform(df[['Purchase']])

    return df

df = load_data()

# ------------------------------
# SIDEBAR
page = st.sidebar.radio("Navigation", [
    "Scope","EDA","Clustering","Association","Anomaly","Final"
])

# ------------------------------
# SCOPE
if page == "Scope":
    st.markdown('<div class="main-header">Black Friday Intelligence</div>', unsafe_allow_html=True)
    
    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Transactions</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-value">${df.Purchase.mean():.0f}</div><div class="metric-label">Avg Spend</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-value">{df.User_ID.nunique()}</div><div class="metric-label">Customers</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    🎯 Goal: Understand customer behavior and maximize revenue using data mining.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# EDA
elif page == "EDA":
    fig = px.box(df, x="Age", y="Purchase", color="Gender",
                 color_discrete_map={'Male':'#00E5FF','Female':'#A259FF'},
                 template='plotly_dark')
    st.plotly_chart(fig)

    show_insight("Customers aged 26-35 and 36-45 dominate spending patterns.")

# ------------------------------
# CLUSTERING
elif page == "Clustering":
    X = df[['Age_Code','Purchase_Scaled']]
    k = st.slider("Clusters",2,5,3)

    model = KMeans(n_clusters=k,n_init=10)
    df['Cluster'] = model.fit_predict(X)

    avg = df.groupby('Cluster')['Purchase'].mean().sort_values()

    labels = ["Low","Mid","High","VIP","Elite"]
    mapping = {c:labels[i] for i,c in enumerate(avg.index)}
    df['Segment'] = df['Cluster'].map(mapping)

    fig = px.scatter(df, x="Age", y="Purchase", color="Segment",
                     template='plotly_dark')
    st.plotly_chart(fig)

    show_insight("High-value clusters represent premium customers for targeting.")

# ------------------------------
# ASSOCIATION
elif page == "Association":
    transactions = df[['Product_Category_1','Product_Category_2']].values.tolist()

    te = TransactionEncoder()
    df_te = pd.DataFrame(te.fit(transactions).transform(transactions),
                         columns=te.columns_)

    freq = apriori(df_te, min_support=0.05, use_colnames=True)

    if not freq.empty:
        rules = association_rules(freq, metric="lift", min_threshold=1)
        rules = rules.sort_values("lift", ascending=False).head(5)

        st.dataframe(rules)

        show_insight("Strong product bundles reveal cross-selling opportunities.")

# ------------------------------
# ANOMALY
elif page == "Anomaly":
    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    upper = Q3 + 1.5*(Q3-Q1)

    df['Type'] = np.where(df['Purchase']>upper,"Outlier","Normal")

    fig = px.histogram(df, x="Purchase", color="Type",
                       template='plotly_dark')
    st.plotly_chart(fig)

    show_insight("Outliers represent high-value customers worth retaining.")

# ------------------------------
# FINAL
elif page == "Final":
    st.markdown('<div class="main-header">Final Business Strategy</div>', unsafe_allow_html=True)

    show_insight("Target high-value clusters for maximum ROI.")
    show_insight("Bundle products with strong association rules.")
    show_insight("Retain outliers as VIP customers.")

# ------------------------------
# FOOTER
st.markdown('<div class="footer">Built with ❤️ | Black Friday Intelligence</div>', unsafe_allow_html=True)
