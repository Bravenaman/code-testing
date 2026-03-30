import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# ------------------ CONFIG ------------------
st.set_page_config(page_title="AI Retail Intelligence", layout="wide")

# ------------------ UI ------------------
st.markdown("""
<style>
body {background: linear-gradient(135deg, #020617, #0f172a);}
.main-header {
    font-size: 3rem; font-weight: 900; text-align: center;
    color: #00E5FF; padding: 20px; border-radius: 15px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
}
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px; padding: 20px;
    margin-bottom: 20px;
}
.metric {font-size: 2rem; color:#00E5FF;}
.insight {
    background: rgba(0,229,255,0.1);
    border-left: 5px solid #00E5FF;
    padding: 15px; border-radius: 10px;
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
        "Category": np.random.choice(['Electronics','Apparel','Home','Beauty'], n),
        "Purchase": np.abs(np.random.normal(9000,3000,n))
    })

    df.loc[df['Age']=='26-35','Purchase'] += 3000
    df.loc[df['Age']=='36-45','Purchase'] += 4000

    df['Age_Code'] = df['Age'].map({'18-25':1,'26-35':2,'36-45':3,'46-50':4})

    scaler = StandardScaler()
    df['Scaled'] = scaler.fit_transform(df[['Purchase']])

    return df

df = load()

# ------------------ FILTERS ------------------
st.sidebar.title("🎛️ Controls")

age_filter = st.sidebar.multiselect("Age", df['Age'].unique(), df['Age'].unique())
gender_filter = st.sidebar.multiselect("Gender", df['Gender'].unique(), df['Gender'].unique())
cat_filter = st.sidebar.multiselect("Category", df['Category'].unique(), df['Category'].unique())

df = df[
    (df['Age'].isin(age_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['Category'].isin(cat_filter))
]

# ------------------ NAVIGATION ------------------
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

# ------------------ KPI ------------------
c1,c2,c3 = st.columns(3)
c1.markdown(f'<div class="glass"><div class="metric">${df.Purchase.sum():,.0f}</div>Total Revenue</div>', unsafe_allow_html=True)
c2.markdown(f'<div class="glass"><div class="metric">${df.Purchase.mean():,.0f}</div>Avg Spend</div>', unsafe_allow_html=True)
c3.markdown(f'<div class="glass"><div class="metric">{len(df)}</div>Transactions</div>', unsafe_allow_html=True)

# ------------------ STAGE 1 ------------------
if page == "Stage 1: Scope":
    st.markdown('<div class="glass">🎯 Goal: Turn raw data into business decisions using analytics.</div>', unsafe_allow_html=True)

# ------------------ STAGE 2 ------------------
elif page == "Stage 2: Preprocessing":
    st.markdown('<div class="glass">Data cleaned, encoded, and scaled.</div>', unsafe_allow_html=True)
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

    avg = df.groupby('Cluster')['Purchase'].mean().sort_values()
    labels = ["Low","Mid","High","VIP","Elite"]
    mapping = {c:labels[i] for i,c in enumerate(avg.index)}
    df['Segment'] = df['Cluster'].map(mapping)

    fig = px.scatter(df, x="Age", y="Purchase", color="Segment",
                     template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    insight("High-value segments drive most revenue.")

# ------------------ STAGE 5 ------------------
elif page == "Stage 5: Association":

    st.markdown("### 📚 Student Behavior Pattern Mining")

    # ------------------ CONTROLS ------------------
    support = st.slider("Minimum Support", 0.01, 0.3, 0.05)
    confidence = st.slider("Minimum Confidence", 0.1, 1.0, 0.5)

    # ------------------ CREATE STUDENT DATA (IF NOT PRESENT) ------------------
    # Simulating realistic student features
    df['Study_Level'] = pd.cut(df['Purchase'],
                              bins=3,
                              labels=['Low Study', 'Medium Study', 'High Study'])

    df['Performance'] = pd.cut(df['Purchase'],
                              bins=3,
                              labels=['Low Score', 'Average Score', 'High Score'])

    # ------------------ BUILD TRANSACTIONS ------------------
    transactions = []

    for _, row in df.iterrows():
        basket = [
            f"Study={row['Study_Level']}",
            f"Performance={row['Performance']}",
            f"Age={row['Age']}",
            f"Gender={row['Gender']}"
        ]
        transactions.append(basket)

    # ------------------ ENCODING ------------------
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df_te = pd.DataFrame(te_array, columns=te.columns_)

    # ------------------ APRIORI ------------------
    freq = apriori(df_te, min_support=support, use_colnames=True)

    if not freq.empty:
        rules = association_rules(freq, metric="confidence", min_threshold=confidence)

        if not rules.empty:
            # Clean and format rules
            rules = rules.sort_values("lift", ascending=False)

            rules['Rule'] = rules['antecedents'].apply(lambda x: list(x)[0]) + " → " + \
                            rules['consequents'].apply(lambda x: list(x)[0])

            st.markdown("### 🔗 Top Patterns Discovered")
            st.dataframe(rules[['Rule', 'support', 'confidence', 'lift']].head(10))

            # ------------------ INSIGHT ------------------
            top_rule = rules.iloc[0]['Rule']

            st.success(f"""
            📌 Key Insight:

            Strongest Pattern Found:
            {top_rule}

            This indicates a strong relationship between these student behaviors.
            """)

        else:
            st.warning("No strong rules found. Try lowering confidence.")
    else:
        st.warning("No frequent patterns found. Try lowering support.")

# ------------------ STAGE 6 ------------------
elif page == "Stage 6: Anomaly":
    mult = st.slider("Sensitivity",1.0,3.0,1.5)

    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    upper = Q3 + mult*(Q3-Q1)

    df['Type'] = np.where(df['Purchase']>upper,"VIP","Normal")

    fig = px.histogram(df, x="Purchase", color="Type",
                       template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    insight("Higher sensitivity reduces VIP classification.")

# ------------------ STAGE 7 ------------------
elif page == "Stage 7: Final":
    st.markdown("### 🧠 Decision Engine")

    if len(df) > 0:
        top_age = df.groupby('Age')['Purchase'].mean().idxmax()

        st.success(f"""
        📌 Based on your filters:

        • Target Age Group: {top_age}  
        • Strategy: Focus marketing here  
        • Action: Bundle high-performing categories  
        """)

    insight("Use filters to simulate different business strategies.")

# ------------------ FOOTER ------------------
st.markdown('<div class="glass">🚀 Built as an interactive decision-making system</div>', unsafe_allow_html=True)
