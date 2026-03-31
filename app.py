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

# ------------------ CLEAN UI ------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.header {
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    color: #38BDF8;
    margin-bottom: 30px;
}

.card {
    background: #0F172A;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 20px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: bold;
    color: #38BDF8;
}

.kpi-label {
    color: #94A3B8;
}

.insight {
    background: rgba(56,189,248,0.08);
    border-left: 4px solid #38BDF8;
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
}

.section {
    font-size: 1.3rem;
    color: #E5E7EB;
    margin-bottom: 10px;
}

/* -------- NEW DUAL CARD -------- */
.dual-card {
    background: linear-gradient(145deg, #111827, #1F2937);
    padding: 25px;
    border-radius: 18px;
    border-left: 6px solid #38BDF8;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    height: 100%;
}

.dual-card h3 {
    color: #E5E7EB;
    margin-bottom: 15px;
}

.dual-card ul {
    padding-left: 20px;
}

.dual-card li {
    margin-bottom: 10px;
    color: #CBD5F5;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------ UI FUNCTIONS ------------------
def header(text):
    st.markdown(f'<div class="header">{text}</div>', unsafe_allow_html=True)

def card(text):
    st.markdown(f'<div class="card">{text}</div>', unsafe_allow_html=True)

def kpi(label, value):
    st.markdown(f"""
    <div class="card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section">{text}</div>', unsafe_allow_html=True)

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

# ------------------ SIDEBAR ------------------
st.sidebar.title("🎛️ Controls")

age_filter = st.sidebar.multiselect("Age", df['Age'].unique(), df['Age'].unique())
gender_filter = st.sidebar.multiselect("Gender", df['Gender'].unique(), df['Gender'].unique())
cat_filter = st.sidebar.multiselect("Category", df['Category'].unique(), df['Category'].unique())

df = df[
    (df['Age'].isin(age_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['Category'].isin(cat_filter))
]

page = st.sidebar.radio("📊 Navigation", [
    "Stage 1: Project Scope",
    "Stage 2: Data Preprocessing",
    "Stage 3: EDA",
    "Stage 4: Clustering Analysis",
    "Stage 5: Association Rules",
    "Stage 6: Anomaly Detection",
    "Stage 7: Insights & Reporting"
])

# ------------------ HEADER ------------------
header("🛍️ AI Retail Intelligence System")

c1, c2, c3 = st.columns(3)
with c1:
    kpi("Total Revenue", f"${df.Purchase.sum():,.0f}")
with c2:
    kpi("Avg Spend", f"${df.Purchase.mean():,.0f}")
with c3:
    kpi("Transactions", len(df))

# ------------------ STAGE 1 ------------------
if page == "Stage 1: Project Scope":
    section("📋 Stage 1: Project Scope, Objectives & Tasks")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="dual-card">
            <h3>🎯 Project Objectives</h3>
            <ul>
                <li><b>Primary Goal:</b> Analyze Black Friday sales data to uncover hidden consumer trends, segment customers by purchasing behavior, and identify high-value product combinations.</li>
                <li><b>Outcome:</b> Deliver actionable business insights that help retailers optimize inventory, improve targeting strategies, and increase overall revenue.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="dual-card">
            <h3>🗺️ Project Scope & Tasks</h3>
            <ul>
                <li><b>Data Preprocessing:</b> Clean and prepare raw transactional data.</li>
                <li><b>EDA:</b> Explore patterns between demographics and spending.</li>
                <li><b>Clustering:</b> Segment customers into meaningful groups.</li>
                <li><b>Association Rules:</b> Identify cross-selling opportunities.</li>
                <li><b>Anomaly Detection:</b> Detect high-value outlier customers.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ------------------ REST OF CODE SAME ------------------
elif page == "Stage 2: Data Preprocessing":
    card("Data cleaned, encoded, and scaled.")
    st.dataframe(df.head())

elif page == "Stage 3: EDA":
    section("Purchase Distribution")
    fig = px.box(df, x="Age", y="Purchase", color="Gender", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    top_age = df.groupby('Age')['Purchase'].mean().idxmax()
    insight(f"Highest spending group is {top_age}.")
    
    # ------------------------------
    # Most Popular Product Categories
    st.markdown("### 2. Most Popular Product Categories")

    cat_counts = df['Category'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Number of Purchases']

    fig2 = px.bar(
        cat_counts,
        x='Category',
        y='Number of Purchases',
        color='Category',
        template='plotly_dark'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ------------------------------
    # Average Purchase per Category
    st.markdown("### 3. Average Purchase per Category")

    cat_avg = df.groupby('Category')['Purchase'].mean().reset_index()

    fig3 = px.bar(
        cat_avg,
        x='Category',
        y='Purchase',
        color='Purchase',
        color_continuous_scale='viridis',
        template='plotly_dark'
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ------------------------------
    # Scatter Plot: Purchase vs Occupation
    st.markdown("### 4. Scatter Plot: Purchase vs. Occupation")

    fig4 = px.scatter(
        df,
        x='Occupation',
        y='Purchase',
        color='Gender',
        opacity=0.6,
        template='plotly_dark'
    )

    st.plotly_chart(fig4, use_container_width=True)
    

elif page == "Stage 4: Clustering Analysis":
    k = st.slider("Clusters",2,5,3)
    X = df[['Age_Code','Scaled']]
    model = KMeans(n_clusters=k,n_init=10)
    df['Cluster'] = model.fit_predict(X)
    avg = df.groupby('Cluster')['Purchase'].mean().sort_values()
    labels = ["Low","Mid","High","VIP","Elite"]
    mapping = {c:labels[i] for i,c in enumerate(avg.index)}
    df['Segment'] = df['Cluster'].map(mapping)
    fig = px.scatter(df, x="Age", y="Purchase", color="Segment", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    insight("High-value segments drive most revenue.")

elif page == "Stage 5: Association Rules":
    support = st.slider("Support",0.01,0.2,0.05)
    confidence = st.slider("Confidence",0.1,1.0,0.5)

    transactions = []
    for _, row in df.iterrows():
        basket = [
            f"Category={row['Category']}",
            f"Age={row['Age']}",
            f"Gender={row['Gender']}"
        ]
        transactions.append(basket)

    te = TransactionEncoder()
    df_te = pd.DataFrame(te.fit(transactions).transform(transactions), columns=te.columns_)

    freq = apriori(df_te, min_support=support, use_colnames=True)

    if not freq.empty:
        rules = association_rules(freq, metric="confidence", min_threshold=confidence)
        st.dataframe(rules)
        insight("Adjust sliders to discover relationships.")

elif page == "Stage 6: Anomaly Detection":
    mult = st.slider("Sensitivity",1.0,3.0,1.5)
    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    upper = Q3 + mult*(Q3-Q1)
    df['Type'] = np.where(df['Purchase']>upper,"VIP","Normal")
    fig = px.histogram(df, x="Purchase", color="Type", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    insight("Higher sensitivity reduces VIP classification.")

elif page == "Stage 7: Insights & Reporting":
    st.markdown("### 🧠 Decision Engine")
    if len(df) > 0:
        top_age = df.groupby('Age')['Purchase'].mean().idxmax()
        st.success(f"""
        📌 Based on your filters:

        • Target Age Group: {top_age}  
        • Strategy: Focus marketing here  
        • Action: Bundle high-performing categories  
        """)
    insight("Use filters to simulate strategies.")
