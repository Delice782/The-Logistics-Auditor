import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Veridi Logistics Auditor", layout="wide")

st.title("Veridi Logistics — Last Mile Delivery Audit")
st.caption("Olist Brazilian E-Commerce Dataset | AmaliTech Practical Capstone Challenge")

@st.cache_data
def load_data():
    file_id = '1TWbJodlctgH0XOrEXA6emUoz2nsqYNca'
    url = f'https://drive.google.com/uc?id={file_id}'
    df = pd.read_csv(url)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    return df

df = load_data()

total = len(df)
late_pct = df['is_late'].sum() / total * 100
avg_review = df['review_score'].mean()

st.subheader("Key Metrics")
k1, k2, k3 = st.columns(3)
k1.metric("Total Orders", f"{total:,}")
k2.metric("Late Delivery Rate", f"{late_pct:.1f}%")
k3.metric("Avg Review Score", f"{avg_review:.2f} / 5")

st.subheader("Late Delivery Rate by State")

state_stats = (
    df.groupby('customer_state')
    .agg(total=('order_id', 'count'), late=('is_late', 'sum'))
    .assign(late_pct=lambda d: d['late'] / d['total'] * 100)
    .sort_values('late_pct', ascending=False)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(state_stats['customer_state'], state_stats['late_pct'], color='coral', edgecolor='black')
ax.axhline(y=state_stats['late_pct'].mean(), color='red', linestyle='--',
           linewidth=2, label=f'National Average: {state_stats["late_pct"].mean():.1f}%')
ax.set_xlabel('State')
ax.set_ylabel('Late Delivery %')
ax.set_title('Late Delivery Rate by State')
plt.xticks(rotation=45, ha='right')
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.subheader("Average Review Score by Delivery Status")

avg_by_status = (
    df.groupby('delivery_status')['review_score']
    .mean()
    .reindex(['On Time', 'Late', 'Super Late'])
    .dropna()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(7, 5))
colors = ['green', 'orange', 'red']
bars = ax.bar(avg_by_status['delivery_status'], avg_by_status['review_score'],
              color=colors, edgecolor='black', width=0.5)
for bar, val in zip(bars, avg_by_status['review_score']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
            f'{val:.2f}', ha='center', fontweight='bold')
ax.set_ylim(0, 5.5)
ax.set_ylabel('Average Review Score')
ax.set_title('Average Review Score by Delivery Status')
ax.axhline(y=df['review_score'].mean(), color='red', linestyle='--',
           linewidth=2, label=f'Overall Average: {df["review_score"].mean():.2f}')
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.subheader("Delivery Delay vs Review Score")

scatter_data = df[df['review_score'].notna() & df['Days_Difference'].notna()]
delay_sentiment = scatter_data.groupby('Days_Difference')['review_score'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.scatter(delay_sentiment['Days_Difference'], delay_sentiment['review_score'],
           color='coral', alpha=0.5)
ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Estimated Delivery Date')
ax.set_xlabel('Days Difference (positive = early, negative = late)')
ax.set_ylabel('Average Review Score')
ax.set_title('Delivery Delay vs Average Review Score')
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.subheader("Monthly Late Delivery Rate Over Time")

monthly = (
    df.groupby('order_year_month')
    .agg(total_orders=('order_id', 'count'), late_orders=('is_late', 'sum'))
    .assign(late_pct=lambda d: d['late_orders'] / d['total_orders'] * 100)
    .reset_index()
)
monthly = monthly[monthly['total_orders'] >= 50]

fig, ax1 = plt.subplots(figsize=(16, 6))
x_labels = monthly['order_year_month']
x = range(len(monthly))

ax1.bar(x, monthly['total_orders'], color='steelblue', alpha=0.5,
        label='Total Orders', edgecolor='black')
ax1.set_ylabel('Total Orders', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

ax2 = ax1.twinx()
ax2.plot(x, monthly['late_pct'], color='red', marker='o',
         linewidth=2.5, markersize=6, label='Late Delivery %')
ax2.set_ylabel('Late Delivery %', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.axhline(y=monthly['late_pct'].mean(), color='red', linestyle='--',
            linewidth=2, alpha=0.7, label=f'Average: {monthly["late_pct"].mean():.1f}%')

ax1.set_xticks(list(x))
ax1.set_xticklabels(x_labels, rotation=45, ha='right')
ax1.set_title('Monthly Late Delivery Rate Over Time')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.subheader("Late Rate by Product Category")

cat_stats = (
    df[df['product_category_name_english'].notna()]
    .groupby('product_category_name_english')
    .agg(total=('order_id', 'count'), late=('is_late', 'sum'))
    .query('total >= 100')
    .assign(late_pct=lambda d: d['late'] / d['total'] * 100)
    .sort_values('late_pct', ascending=False)
    .reset_index()
    .head(10)
)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(cat_stats['product_category_name_english'], cat_stats['late_pct'],
              color='goldenrod', edgecolor='black')
for bar, val in zip(bars, cat_stats['late_pct']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
            f'{val:.1f}%', ha='center')
ax.axhline(y=cat_stats['late_pct'].mean(), color='red', linestyle='--',
           linewidth=2, label=f'Category Average: {cat_stats["late_pct"].mean():.1f}%')
ax.set_xlabel('Product Category')
ax.set_ylabel('Late Delivery %')
ax.set_title('Top 10 Product Categories with Highest Late Delivery Rate')
plt.xticks(rotation=45, ha='right')
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.caption("Built for AmaliTech Capstone — Veridi Logistics Audit")
