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
        "Age": np.random.choice(['18-25','26-35','36-45','46-50'], n),
        "Gender": np.random.choice(['Male','Female'], n),
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

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.title("🎛️ Controls")

age_filter = st.sidebar.multiselect("Age Filter", df['Age'].unique(), default=df['Age'].unique())
gender_filter = st.sidebar.multiselect("Gender Filter", df['Gender'].unique(), default=df['Gender'].unique())

df = df[(df['Age'].isin(age_filter)) & (df['Gender'].isin(gender_filter))]

# ------------------ HEADER ------------------
st.markdown('<div class="main-header">🛍️ AI Retail Intelligence System</div>', unsafe_allow_html=True)

# ------------------ KPIs ------------------
c1,c2,c3 = st.columns(3)
c1.markdown(f'<div class="glass"><div class="metric">${df.Purchase.sum():,.0f}</div>Total Revenue</div>', unsafe_allow_html=True)
c2.markdown(f'<div class="glass"><div class="metric">${df.Purchase.mean():,.0f}</div>Avg Spend</div>', unsafe_allow_html=True)
c3.markdown(f'<div class="glass"><div class="metric">{len(df)}</div>Transactions</div>', unsafe_allow_html=True)

# ------------------ EDA ------------------
st.markdown("### 📊 Spending Patterns")

fig = px.box(df, x="Age", y="Purchase", color="Gender",
             color_discrete_map={'Male':'#00E5FF','Female':'#A259FF'},
             template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

top_age = df.groupby('Age')['Purchase'].mean().idxmax()
insight(f"Highest spending group is {top_age}, making them the primary revenue drivers.")

# ------------------ CLUSTERING ------------------
st.markdown("### 🎯 Customer Segments")

k = st.slider("Clusters",2,5,3)

X = df[['Age_Code','Scaled']]
model = KMeans(n_clusters=k,n_init=10)
df['Cluster'] = model.fit_predict(X)

cluster_avg = df.groupby('Cluster')['Purchase'].mean().sort_values()

labels = ["Low","Mid","High","VIP","Elite"]
mapping = {c:labels[i] for i,c in enumerate(cluster_avg.index)}
df['Segment'] = df['Cluster'].map(mapping)

fig2 = px.scatter(df, x="Age", y="Purchase", color="Segment",
                  template='plotly_dark')
st.plotly_chart(fig2, use_container_width=True)

insight("High-value clusters represent premium customers — target them for maximum ROI.")

# ------------------ ASSOCIATION ------------------
st.markdown("### 🛒 Product Intelligence")

transactions = df[['Category']].values.tolist()
te = TransactionEncoder()
df_te = pd.DataFrame(te.fit(transactions).transform(transactions), columns=te.columns_)

freq = apriori(df_te, min_support=0.1, use_colnames=True)

if not freq.empty:
    rules = association_rules(freq, metric="lift", min_threshold=1)
    st.dataframe(rules.head(5))

    insight("Product combinations reveal strong bundling opportunities.")

# ------------------ ANOMALY ------------------
st.markdown("### 🚨 High-Value Customers")

Q1 = df['Purchase'].quantile(0.25)
Q3 = df['Purchase'].quantile(0.75)
upper = Q3 + 1.5*(Q3-Q1)

df['Type'] = np.where(df['Purchase']>upper,"VIP","Normal")

fig3 = px.histogram(df, x="Purchase", color="Type",
                    template='plotly_dark')
st.plotly_chart(fig3, use_container_width=True)

insight("VIP customers (outliers) should be retained with loyalty rewards.")

# ------------------ FINAL ------------------
st.markdown("### 💡 AI Strategy Engine")

insight("Focus marketing on high-value segments instead of general users.")
insight("Use product bundling to increase average order value.")
insight("Retain VIP customers to maximize long-term revenue.")
