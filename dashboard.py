import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "tech_gadgets_cleaned.csv"
df = pd.read_csv(file_path)

# Streamlit Page Config
st.set_page_config(page_title="E-commerce Sales Dashboard", layout="wide")

# Sidebar - Filters
st.sidebar.header("🔎 Filter Data")

# ---- Category Filter with "All" Option ----
categories = ["All"] + list(df['category'].unique())
selected_category = st.sidebar.multiselect("Select Category", categories, default="All")

if "All" in selected_category:
    category_filter = df['category'].unique()
else:
    category_filter = selected_category

# ---- Brand Filter with "All" Option ----
brands = ["All"] + list(df['brand'].unique())
selected_brand = st.sidebar.multiselect("Select Brand", brands, default="All")

if "All" in selected_brand:
    brand_filter = df['brand'].unique()
else:
    brand_filter = selected_brand

# Apply filters
filtered_df = df[df['category'].isin(category_filter) & df['brand'].isin(brand_filter)]

# --- Dashboard Title ---
st.title("📊 E-commerce Analytics Dashboard")

# --- Metrics Section ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales (Units)", filtered_df['bought'].sum())
col2.metric("Total Revenue (₹)", f"{(filtered_df['bought'] * filtered_df['price']).sum():,.2f}")
col3.metric("Average Product Rating", round(filtered_df['rating'].mean(), 2))

# --- 1. Top 10 Best-Selling Products ---
st.subheader("🏆 Top 10 Best-Selling Products")
top_selling = filtered_df.nlargest(10, 'bought')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_selling['title'].str[:30] + "...", x=top_selling['bought'], hue=top_selling['title'], palette="viridis", legend=False, ax=ax)
ax.set_xlabel("Units Sold")
ax.set_ylabel("Product")
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# --- 2. Category-Wise Sales Distribution ---
st.subheader("📌 Category-Wise Sales Distribution")
category_sales = filtered_df.groupby('category')['bought'].sum()

fig, ax = plt.subplots(figsize=(6, 6))
category_sales.plot.pie(autopct='%1.1f%%', colors=sns.color_palette("pastel"), startangle=140, ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# --- 3. Top 10 Brands by Sales ---
st.subheader("🔥 Top 10 Brands by Sales")
brand_sales = filtered_df.groupby('brand')['bought'].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=brand_sales.index, y=brand_sales.values, hue=brand_sales.index, palette="coolwarm", legend=False, ax=ax)
ax.set_xlabel("Brand")
ax.set_ylabel("Total Units Sold")
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# --- 4. Discount vs. Units Sold ---
st.subheader("💰 Impact of Discount on Sales")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=filtered_df['off'], y=filtered_df['bought'], hue=filtered_df['category'], palette="deep", alpha=0.7, ax=ax)
ax.set_xlabel("Discount Percentage (%)")
ax.set_ylabel("Units Sold")
ax.axhline(filtered_df['bought'].mean(), color='red', linestyle="dashed", label="Avg Sales")
plt.legend(fontsize=9)
st.pyplot(fig)

# --- 5. Price vs. Units Sold ---
st.subheader("💲 Price vs. Sales Trend")
fig, ax = plt.subplots(figsize=(10, 5))
sns.regplot(x=filtered_df['price'], y=filtered_df['bought'], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax)
ax.set_xlabel("Price (INR)")
ax.set_ylabel("Units Sold")
st.pyplot(fig)

# --- 6. Top 10 Highest Rated Products ---
st.subheader("⭐ Top 10 Highest Rated Products")
top_rated = filtered_df[filtered_df['rating'] > 0].nlargest(10, 'rating')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_rated['title'].str[:30] + "...", x=top_rated['rating'], hue=top_rated['title'], palette="magma", legend=False, ax=ax)
ax.set_xlabel("Average Rating")
ax.set_ylabel("Product")
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# --- 7. Rating Distribution Across Categories ---
st.subheader("📊 Rating Distribution Across Categories")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=filtered_df['category'], y=filtered_df['rating'], hue=filtered_df['category'], palette="Set2", legend=False, ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Ratings")
st.pyplot(fig)

# --- 8. Download Filtered Data ---
st.subheader("📥 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data as CSV", csv, "filtered_data.csv", "text/csv", key="download-csv")

# --- 9. Product Search Feature ---
st.subheader("🔍 Search for a Product")
search_query = st.text_input("Enter product name:")
if search_query:
    search_results = filtered_df[filtered_df['title'].str.contains(search_query, case=False, na=False)]
    st.write(f"Found {len(search_results)} products matching **{search_query}**")
    st.dataframe(search_results)

# --- 10. Show Raw Data ---
st.subheader("📋 Raw Data")
st.dataframe(filtered_df)
