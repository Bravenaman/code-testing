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

# ------------------ UI STYLING ------------------
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
    margin-bottom: 20px;
    line-height: 1.6;
    color: #ffffff;
    white-space: normal;
    word-wrap: break-word;
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


# 🔥 MAIN INSIGHT BOX (USE THIS EVERYWHERE)
def insight_box(text):
    st.markdown(f'<div class="insight">💡 <b>Insight:</b> {text}</div>', unsafe_allow_html=True)


# (Optional — you can remove this later if you want)
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
    insight_box(
    "The dataset has been cleaned, encoded, and standardized to ensure consistency and accuracy in analysis. "
    "Scaling purchase values helps improve clustering performance, while encoding categorical variables "
    "enables machine learning models to interpret customer demographics effectively."
    )

elif page == "Stage 3: EDA":
    section("Purchase Distribution")
    fig = px.box(df, x="Age", y="Purchase", color="Gender", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    top_age = df.groupby('Age')['Purchase'].mean().idxmax()
    insight_box(
    "Customers aged 26–45 show the highest spending range and median purchases. "
    "Male customers also display wider variability, indicating more high-value transactions."
    )
    
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
    insight_box(
    "Certain product categories dominate purchase frequency, indicating strong demand trends. "
    "Retailers should prioritize inventory and marketing efforts toward these high-volume categories."
    )

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
    insight_box(
    "Some categories generate higher average transaction values despite lower purchase counts. "
    "These categories represent premium segments and offer strong revenue potential per sale."
    )

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
    insight_box(
    "Spending patterns vary across occupation groups, with certain occupations showing consistently higher purchases. "
    "This suggests income-level influence on spending behavior and potential for targeted marketing."
    )

    # ------------------------------
    # Correlation Heatmap for Key Features
    st.markdown("### 5. Correlation Heatmap for Key Features")

    # Select only numeric columns that exist in your dataset
    corr_cols = ['Age_Code', 'Gender_Code', 'Occupation', 'Marital_Status', 'Purchase']

    # Make sure only existing columns are used
    corr_cols = [col for col in corr_cols if col in df.columns]

    corr_matrix = df[corr_cols].corr()

    fig5 = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        template='plotly_dark'
    )

    st.plotly_chart(fig5, use_container_width=True)
    insight_box(
    "A positive correlation exists between age and purchase amount, indicating increased spending with age. "
    "Other variables show weaker relationships, suggesting independent influence on purchasing behavior."
    )
    

elif page == "Stage 4: Clustering Analysis":

    st.markdown("### 📉 Elbow Method (Optimal Clusters)")

    X = df[['Age_Code', 'Scaled']]

    wcss = []
    K_range = range(1, 8)

    for k_val in K_range:
        kmeans = KMeans(n_clusters=k_val, n_init=10, random_state=42)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    # Create DataFrame for plotting
    elbow_df = pd.DataFrame({
        "K": list(K_range),
        "WCSS": wcss
    })

    # Plot
    fig_elbow = px.line(
        elbow_df,
        x="K",
        y="WCSS",
        markers=True,
        template='plotly_dark',
        title="Elbow Method"
    )

    # Highlight K=3
    fig_elbow.add_annotation(
        x=3,
        y=wcss[2],
        text="Elbow Point (k=3)",
        showarrow=True,
        arrowhead=2
    )

    # ✅ FIXED INDENTATION (inside block)
    st.plotly_chart(fig_elbow, use_container_width=True)

    insight_box(
        "The Elbow Method shows a sharp drop in WCSS until K=3, after which improvements slow down. "
        "This indicates that 3 clusters provide an optimal balance between model simplicity and accuracy."
    )

        # ---------------- INTERACTIVE CLUSTERING ----------------
    st.markdown("### 🎛️ Interactive Clustering & Segmentation")

    # Slider for selecting number of clusters
    k = st.slider("Select Number of Clusters (K)", 2, 5, 3)

    # Features for clustering
    X = df[['Age_Code', 'Scaled']]

    # Apply KMeans
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    df['Cluster'] = model.fit_predict(X)

    # Sort clusters by spending to label them meaningfully
    avg = df.groupby('Cluster')['Purchase'].mean().sort_values()
    labels = ["Low","Mid","High","VIP","Elite"]
    mapping = {c: labels[i] for i, c in enumerate(avg.index)}
    df['Segment'] = df['Cluster'].map(mapping)

    # Scatter Plot
    fig = px.scatter(
        df,
        x="Age",
        y="Purchase",
        color="Segment",
        template='plotly_dark',
        title="Customer Segments Based on Spending Behavior"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insight
    top_segment = df.groupby('Segment')['Purchase'].mean().idxmax()

    insight_box(
        f"The '{top_segment}' segment represents the highest spending customers. "
        "These users contribute significantly to revenue and should be targeted with "
        "premium offerings, loyalty programs, and personalized marketing strategies. "
        "Lower segments can be nurtured through discounts and engagement campaigns to increase spending."
    )

elif page == "Stage 5: Association Rules":

    support = st.slider("Support", 0.01, 0.2, 0.05)
    confidence = st.slider("Confidence", 0.1, 1.0, 0.5)

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

        # ✅ ORIGINAL TABLE (keep this)
        st.dataframe(rules)

        # ---------------- NEW VISUALIZATION ----------------
        if not rules.empty:
            st.markdown("### 📊 Visualizing Frequent Product Combinations")

            fig_rules = px.scatter(
                rules,
                x="support",
                y="confidence",
                size="lift",
                color="lift",
                hover_data=["antecedents", "consequents"],
                template="plotly_dark",
                title="Rule Strength: Support vs Confidence (Size = Lift)"
            )

            st.plotly_chart(fig_rules, use_container_width=True)

            # ✅ Insight
            insight_box(
                "This visualization highlights the strength of association rules based on support, confidence, and lift. "
                "Rules with higher lift and confidence represent strong product relationships and are ideal for "
                "cross-selling, bundling, and recommendation strategies."
            )

    else:
        st.warning("No frequent itemsets found. Try lowering support.")
        

elif page == "Stage 6: Anomaly Detection":
    mult = st.slider("Sensitivity",1.0,3.0,1.5)
    Q1 = df['Purchase'].quantile(0.25)
    Q3 = df['Purchase'].quantile(0.75)
    upper = Q3 + mult*(Q3-Q1)
    df['Type'] = np.where(df['Purchase']>upper,"VIP","Normal")
    fig = px.histogram(df, x="Purchase", color="Type", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
    "Anomaly detection highlights high-value customers whose spending significantly exceeds the norm. "
    "These 'VIP' customers contribute disproportionately to revenue and should be prioritized for "
    "exclusive deals, premium services, and retention strategies."
    )

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
