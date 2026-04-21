"""
E-Commerce Customer Purchase Analysis
Python Tasks using pandas

"""

import pandas as pd
import matplotlib.pyplot as plt


# -- Task 1: Load dataset ------------------------------------------------------
df = pd.read_csv('sample.csv')
print("=== Dataset Loaded ===")
print(df)
print()

# -- Task 2: Create column total_purchase -------------------------------------
df['total_purchase'] = df['quantity'] * df['price']
print("=== Dataset with total_purchase column ===")
print(df[['customer_id','customer_name','product','quantity','price','total_purchase']])
print()

# -- Task 3: Identify top customers -------------------------------------------
top_customers = (
    df.groupby(['customer_id', 'customer_name'])['total_purchase']
    .sum()
    .reset_index()
    .sort_values('total_purchase', ascending=False)
    .reset_index(drop=True)
)
top_customers.index += 1  # rank from 1
print("=== Top Customers by Total Spending ===")
print(top_customers.to_string())
print(f"\n🏆 Top Spender: {top_customers.iloc[0]['customer_name']}  "
      f"(₹{top_customers.iloc[0]['total_purchase']:,.0f})")
print()

# -- Task 4: Analyze product popularity ---------------------------------------
product_stats = (
    df.groupby('product')
    .agg(
        total_qty_sold=('quantity', 'sum'),
        num_orders=('customer_id', 'count'),
        total_revenue=('total_purchase', 'sum')
    )
    .sort_values('total_qty_sold', ascending=False)
    .reset_index()
)
print("=== Product Popularity ===")
print(product_stats.to_string(index=False))
print(f"\n🥇 Most Popular Product: {product_stats.iloc[0]['product']} "
      f"({product_stats.iloc[0]['total_qty_sold']} units sold)")
print()

# -- City-wise revenue ---------------------------------------------------------
city_revenue = (
    df.groupby('city')['total_purchase']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
city_revenue.columns = ['city', 'total_revenue']
city_revenue['share_%'] = (city_revenue['total_revenue'] /
                            city_revenue['total_revenue'].sum() * 100).round(1)
print("=== City-wise Revenue ===")
print(city_revenue.to_string(index=False))
print()

# -- Visualization 1: Bar chart – Product Sales --------------------------------
prod_rev = product_stats.set_index('product')['total_revenue']
colors = ['#1F4E79','#2E86AB','#A8DADC','#457B9D','#1D3557']

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(prod_rev.index, prod_rev.values,
              color=colors[:len(prod_rev)], edgecolor='white', linewidth=1.2, width=0.55)
for bar, val in zip(bars, prod_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800,
            f'₹{val:,.0f}', ha='center', va='bottom',
            fontsize=10, fontweight='bold', color='#1F4E79')

ax.set_title('Product Sales – Revenue Comparison',
             fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
ax.set_xlabel('Product', fontsize=11); ax.set_ylabel('Total Revenue (₹)', fontsize=11)
ax.set_facecolor('#F8FAFC'); fig.patch.set_facecolor('#FFFFFF')
ax.spines[['top','right']].set_visible(False)
ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#CCCCCC')
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('bar_chart_product_sales.png', dpi=150, bbox_inches='tight')
plt.show()
print("Bar chart saved → bar_chart_product_sales.png")

# -- Visualization 2: Pie chart – City Revenue Distribution -------------------
city_rev = city_revenue.set_index('city')['total_revenue']
pie_colors = ['#1F4E79','#2E86AB','#A8DADC']

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    city_rev.values, labels=None, autopct='%1.1f%%',
    colors=pie_colors[:len(city_rev)], explode=[0.04]*len(city_rev),
    startangle=140, pctdistance=0.75,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
for at in autotexts:
    at.set_fontsize(11); at.set_fontweight('bold'); at.set_color('white')

legend_labels = [f"{c}  –  ₹{v:,.0f}" for c,v in zip(city_rev.index, city_rev.values)]
ax.legend(wedges, legend_labels, title="City", loc="lower center",
          bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=10,
          title_fontsize=11, frameon=False)
ax.set_title('City-wise Revenue Distribution',
             fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
fig.patch.set_facecolor('#FFFFFF')
plt.tight_layout()
plt.savefig('pie_chart_city_revenue.png', dpi=150, bbox_inches='tight')
plt.show()
print("Pie chart saved → pie_chart_city_revenue.png")
